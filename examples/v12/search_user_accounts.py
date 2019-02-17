from auth_helper import *
from customermanagement_example_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):
    
    try:
        output_status_message("-----\nGetUser:")
        get_user_response=customer_service.GetUser(
            UserId=None,
            IncludeLinkedAccountIds=True
        )
        user = get_user_response.User
        customer_roles=get_user_response.CustomerRoles
        output_status_message("User:")
        output_user(user)
        output_status_message("CustomerRoles:")
        output_array_of_customerrole(customer_roles)

        # Search for the accounts that the user can access.
        # To retrieve more than 100 accounts, increase the page size up to 1,000.
        # To retrieve more than 1,000 accounts you'll need to add paging.

        accounts=search_accounts_by_user_id(customer_service, user.Id)

        customer_ids=[]
        for account in accounts['AdvertiserAccount']:
            customer_ids.append(account.ParentCustomerId)
        distinct_customer_ids = {'long': list(set(customer_ids))[:100]}

        for customer_id in distinct_customer_ids['long']:
            # You can find out which pilot features the customer is able to use. 
            # Each account could belong to a different customer, so use the customer ID in each account.
            output_status_message("-----\nGetCustomerPilotFeatures:")
            output_status_message("Requested by CustomerId: {0}".format(customer_id))
            feature_pilot_flags=customer_service.GetCustomerPilotFeatures(
                CustomerId=customer_id
            )
            output_status_message("Customer Pilot flags:")
            output_status_message("; ".join(str(flag) for flag in feature_pilot_flags['int']))
    
    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

# Main execution
if __name__ == '__main__':

    print("Loading the web service client proxies...")
    
    authorization_data=AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    customer_service=ServiceClient(
        service='CustomerManagementService', 
        version=12,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )
        
    authenticate(authorization_data)
        
    main(authorization_data)
