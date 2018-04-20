from auth_helper import *
from customermanagement_example_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):
    
    try:
        # Set to an empty user identifier to get the current authenticated Bing Ads user,
        # and then search for all accounts the user may access.
        get_user_response=customer_service.GetUser(UserId=None)
        user = get_user_response.User
        output_user(user)
        accounts = search_accounts_by_user_id(customer_service, user.Id)

        output_status_message("The user can access the following Bing Ads accounts: \n")
        for account in accounts['Account']:
            customer_service.GetAccount(AccountId=account.Id)
            output_account(account)

            # Optionally you can find out which pilot features the customer is able to use. 
            # Each account could belong to a different customer, so use the customer ID in each account.
            feature_pilot_flags = customer_service.GetCustomerPilotFeatures(CustomerId = account.ParentCustomerId)
            output_status_message("Customer Pilot flags:")
            output_status_message("; ".join(str(flag) for flag in feature_pilot_flags['int']) + "\n")

        output_status_message("Program execution completed")
    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

# Main execution
if __name__ == '__main__':

    print("Python loads the web service proxies at runtime, so you will observe " \
          "a performance delay between program launch and main execution...\n")
    
    authorization_data=AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    customer_service=ServiceClient(
        service='CustomerManagementService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=11,
    )

    # You should authenticate for Bing Ads production services with a Microsoft Account, 
    # instead of providing the Bing Ads username and password set. 
            
    authenticate(authorization_data)
        
    main(authorization_data)
