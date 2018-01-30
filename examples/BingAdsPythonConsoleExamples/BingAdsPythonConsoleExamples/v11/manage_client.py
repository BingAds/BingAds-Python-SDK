import datetime

from auth_helper import *
from customermanagement_example_helper import *

# You must provide credentials in auth_helper.py.

CLIENT_ACCOUNT_ID='ClientAccountIdGoesHere'

def main(authorization_data):

    try:
        output_status_message(
            "You must edit this example to provide the ClientAccountId for the client link." \
            "When adding a client link, the client link's ManagingCustomerId is set to the CustomerId " \
            "of the current authenticated user, who must be a Super Admin of the agency." \
            "Login as an agency Super Admin user to send a client link invitation, or unlink an existing client link." \
            "Login as a client Super Admin user to accept a client link invitation.\n"
        )

        update_client_links_response=None

        # Specify the client link search criteria

        page_info=customer_service.factory.create('ns5:Paging')
        page_info.Index=0  # The first page
        page_info.Size=100 # The first 100 client links for this page of results

        ordering=customer_service.factory.create('ns5:ArrayOfOrderBy')
        order_by=customer_service.factory.create('ns5:OrderBy')
        order_by.Field='Number'
        order_by.Order='Ascending'
        ordering.OrderBy.append(order_by)

        predicates=customer_service.factory.create('ns5:ArrayOfPredicate')
        predicate=customer_service.factory.create('ns5:Predicate')
        predicate.Field='ClientAccountId'
        predicate.Operator='In'
        predicate.Value=CLIENT_ACCOUNT_ID
        predicates.Predicate.append(predicate)

        # Search for client links that match the specified criteria.

        client_links=customer_service.SearchClientLinks(
            Ordering=ordering,
            PageInfo=page_info,
            Predicates=predicates
        )

        '''
        Determine whether the agency is already managing the specified client account. 
        If a link exists with status either Active, LinkInProgress, LinkPending, 
        UnlinkInProgress, or UnlinkPending, the agency may not initiate a duplicate client link.
        '''

        client_link=None
        new_link_required=True

        if len(client_links['ClientLink']) > 0:
            client_link=client_links['ClientLink'][0]
            
            # Reformat the start date to trim tzinfo. This workaround is temporarily required because
            # Customer Management service does not accept signed utc offset e.g. +00:00
            start_date=client_links['ClientLink'][0].StartDate
            reformatted_start_date=(datetime.datetime(
                year=start_date.year, 
                month=start_date.month, 
                day=start_date.day, 
                hour=start_date.hour,
                minute=start_date.minute,
                second=start_date.second,
                microsecond=start_date.microsecond,
                tzinfo=None).isoformat('T'))
            client_link.StartDate=reformatted_start_date
            
            client_links=customer_service.factory.create('ns5:ArrayOfClientLink')
            client_links.ClientLink.append(client_link)
            
            output_status_message("Current ClientLink Status: {0}.\n".format(client_link.Status))

            # The agency may choose to initiate the unlink process, 
            # which would terminate the existing relationship with the client. 
            if client_link.Status == 'Active':
                client_link.Status='UnlinkRequested'
                update_client_links_response=customer_service.UpdateClientLinks(client_links)
                output_status_message("UpdateClientLinks : UnlinkRequested.\n")
                new_link_required=False
            # Waiting on a system status transition or waiting for the StartDate.
            elif client_link.Status == 'LinkAccepted':
                output_status_message("The status is transitioning towards LinkInProgress.\n")
                new_link_required=False
            # Waiting on a system status transition.
            elif client_link.Status == 'LinkInProgress':
                output_status_message("The status is transitioning towards Active.\n")
                new_link_required=False
            # When the status is LinkPending, either the agency or client may update the status.
            # The agency may choose to cancel the client link invitation; however, in this example 
            # the client will accept the invitation. 
            # If the client does not accept or decline the invitation within 30 days, and if the agency
            # does not update the status to LinkCanceled, the system updates the status to LinkExpired.
            elif client_link.Status == 'LinkPending':
                '''
                client_link.Status='LinkCanceled'
                update_client_links_response=customer_service.UpdateClientLinks(client_links)
                output_status_message("UpdateClientLinks: LinkCanceled.\n")
                '''
                client_link.Status='LinkAccepted'
                update_client_links_response=customer_service.UpdateClientLinks(client_links)
                output_status_message("UpdateClientLinks: LinkAccepted.\n")
                new_link_required=False
            # Waiting on a system status transition.
            elif client_link.Status == 'UnlinkInProgress':
                output_status_message("The status is transitioning towards Inactive.\n")
                new_link_required=False
            # Waiting on a system status transition.
            elif client_link.Status == 'UnlinkPending':
                output_status_message("The status is transitioning towards Inactive.\n")
                new_link_required=False
            # The link lifecycle has ended.  
            else:
                output_status_message("A new client link invitation is required.\n")
            

            # Print errors if any occurred when updating the client link.
            if update_client_links_response is not None:
                output_array_of_operationerror(update_client_links_response.OperationErrors)
                for arrayofoperationerror in update_client_links_response.PartialErrors['ArrayOfOperationError']:
                    output_array_of_operationerror(arrayofoperationerror)

        # If no links exist between the agency and specified client account, or a link exists with status  
        # either Inactive, LinkCanceled, LinkDeclined, LinkExpired, or LinkFailed, then the agency must
        # initiate a new client link.

        if new_link_required:
            client_links=customer_service.factory.create('ns5:ArrayOfClientLink')
            client_link=customer_service.factory.create('ns5:ClientLink')
            client_link.ClientAccountId=CLIENT_ACCOUNT_ID
            client_link.ManagingCustomerId=authorization_data.customer_id
            client_link.IsBillToClient=True
            client_link.Name="My Client Link"
            client_link.StartDate=None
            client_link.SuppressNotification=True
            client_link.Status=None
            client_links.ClientLink.append(client_link)
            
            add_client_links_response=customer_service.AddClientLinks(client_links)

            # Print errors if any occurred when adding the client link.

            output_array_of_operationerror(add_client_links_response.OperationErrors)
            for arrayofoperationerror in add_client_links_response.PartialErrors['ArrayOfOperationError']:
                output_array_of_operationerror(arrayofoperationerror)
            output_status_message("The user attempted to add a new ClientLink.\n")
            output_status_message("Login as the client Super Admin to accept the agency's request to manage AccountId {0}.\n".format(CLIENT_ACCOUNT_ID))
        
        # Get and print the current client link

        client_links=customer_service.SearchClientLinks(
            Ordering=ordering,
            PageInfo=page_info,
            Predicates=predicates
        )

        output_array_of_clientlink(client_links)

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
    # Authentication with a Microsoft Account is currently not supported in Sandbox.
        
    authenticate(authorization_data)
        
    main(authorization_data)