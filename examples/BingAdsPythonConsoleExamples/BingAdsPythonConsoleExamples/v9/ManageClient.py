from bingads import *

import sys
import webbrowser
from time import gmtime, strftime
import datetime
from suds import WebFault

# Optionally you can include logging to output traffic, for example the SOAP request and response.

#import logging
#logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)

if __name__ == '__main__':
    print("Python loads the web service proxies at runtime, so you will observe " \
          "a performance delay between program launch and main execution...\n")

    DEVELOPER_TOKEN='DeveloperTokenGoesHere'
    ENVIRONMENT='production'
    
    # If you are using OAuth in production, CLIENT_ID is required and CLIENT_STATE is recommended.
    CLIENT_ID='ClientIdGoesHere'
    CLIENT_STATE='ClientStateGoesHere'

    CLIENT_ACCOUNT_ID='YourClientAccountIdGoesHere'

    authorization_data=AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    customer_service=ServiceClient(
        'CustomerManagementService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=9,
    )

def authenticate_with_username():
    ''' 
    Sets the authentication property of the global AuthorizationData instance with PasswordAuthentication.
    '''
    global authorization_data
    authentication=PasswordAuthentication(
        user_name='UserNameGoesHere',
        password='PasswordGoesHere'
    )

    # Assign this authentication instance to the global authorization_data. 
    authorization_data.authentication=authentication
 
def authenticate_with_oauth():
    ''' 
    Sets the authentication property of the global AuthorizationData instance with OAuthDesktopMobileAuthCodeGrant.
    '''
    global authorization_data

    authentication=OAuthDesktopMobileAuthCodeGrant(
        client_id=CLIENT_ID
    )

    # It is recommended that you specify a non guessable 'state' request parameter to help prevent
    # cross site request forgery (CSRF). 
    authentication.state=CLIENT_STATE

    # Assign this authentication instance to the global authorization_data. 
    authorization_data.authentication=authentication   

    # Register the callback function to automatically save the refresh token anytime it is refreshed.
    # Uncomment this line if you want to store your refresh token. Be sure to save your refresh token securely.
    authorization_data.authentication.token_refreshed_callback=save_refresh_token
    
    refresh_token=get_refresh_token()
    
    try:
        # If we have a refresh token let's refresh it
        if refresh_token is not None:
            authorization_data.authentication.request_oauth_tokens_by_refresh_token(refresh_token)
        else:
            request_user_consent()
    except OAuthTokenRequestException:
        # The user could not be authenticated or the grant is expired. 
        # The user must first sign in and if needed grant the client application access to the requested scope.
        request_user_consent()
    
def request_user_consent():
    global authorization_data

    webbrowser.open(authorization_data.authentication.get_authorization_endpoint(), new=1)
    # For Python 3.x use 'input' instead of 'raw_input'
    if(sys.version_info.major >= 3):
        response_uri=eval(input(
            "You need to provide consent for the application to access your Bing Ads accounts. " \
            "After you have granted consent in the web browser for the application to access your Bing Ads accounts, " \
            "please enter the response URI that includes the authorization 'code' parameter: \n"
        ))
    else:
        response_uri=input(
            "You need to provide consent for the application to access your Bing Ads accounts. " \
            "After you have granted consent in the web browser for the application to access your Bing Ads accounts, " \
            "please enter the response URI that includes the authorization 'code' parameter: \n"
        )

    if authorization_data.authentication.state != CLIENT_STATE:
       raise Exception("The OAuth response state does not match the client request state.")

    # Request access and refresh tokens using the URI that you provided manually during program execution.
    authorization_data.authentication.request_oauth_tokens_by_response_uri(response_uri=response_uri) 

def get_refresh_token():
    ''' 
    Returns a refresh token if stored locally.
    '''
    file=None
    try:
        file=open("refresh.txt")
        line=file.readline()
        file.close()
        return line if line else None
    except IOError:
        if file:
            file.close()
        return None

def save_refresh_token(oauth_tokens):
    ''' 
    Stores a refresh token locally. Be sure to save your refresh token securely.
    '''
    with open("refresh.txt","w+") as file:
        file.write(oauth_tokens.refresh_token)
        file.close()
    return None

def search_accounts_by_user_id(user_id):
    ''' 
    Search for account details by UserId.
    
    :param user_id: The Bing Ads user identifier.
    :type user_id: long
    :return: List of accounts that the user can manage.
    :rtype: ArrayOfAccount
    '''
    global customer_service
   
    paging={
        'Index': 0,
        'Size': 10
    }

    predicates={
        'Predicate': [
            {
                'Field': 'UserId',
                'Operator': 'Equals',
                'Value': user_id,
            },
        ]
    }

    search_accounts_request={
        'PageInfo': paging,
        'Predicates': predicates
    }
        
    return customer_service.SearchAccounts(
        PageInfo = paging,
        Predicates = predicates
    )

def add_client_links(client_links):
    global customer_service
    
    return customer_service.AddClientLinks(
        ClientLinks=client_links
    )

def search_client_links(ordering, page_info, predicates):
    global customer_service
    
    return customer_service.SearchClientLinks(
        Ordering=ordering,
        PageInfo=page_info,
        Predicates=predicates
    ).ClientLinks

def update_client_links(client_links):
    global customer_service
    
    return customer_service.UpdateClientLinks(
        ClientLinks=client_links
    )

def output_status_message(message):
    print(message)

def output_bing_ads_webfault_error(error):
    if hasattr(error, 'ErrorCode'):
        output_status_message("ErrorCode: {0}".format(error.ErrorCode))
    if hasattr(error, 'Code'):
        output_status_message("Code: {0}".format(error.Code))
    if hasattr(error, 'Message'):
        output_status_message("Message: {0}".format(error.Message))
    output_status_message('')

def output_webfault_errors(ex):
    if hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ApiFault') \
        and hasattr(ex.fault.detail.ApiFault, 'OperationErrors') \
        and hasattr(ex.fault.detail.ApiFault.OperationErrors, 'OperationError'):
        api_errors=ex.fault.detail.ApiFault.OperationErrors.OperationError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'AdApiFaultDetail') \
        and hasattr(ex.fault.detail.AdApiFaultDetail, 'Errors') \
        and hasattr(ex.fault.detail.AdApiFaultDetail.Errors, 'AdApiError'):
        api_errors=ex.fault.detail.AdApiFaultDetail.Errors.AdApiError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ApiFaultDetail') \
        and hasattr(ex.fault.detail.ApiFaultDetail, 'BatchErrors') \
        and hasattr(ex.fault.detail.ApiFaultDetail.BatchErrors, 'BatchError'):
        api_errors=ex.fault.detail.ApiFaultDetail.BatchErrors.BatchError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ApiFaultDetail') \
        and hasattr(ex.fault.detail.ApiFaultDetail, 'OperationErrors') \
        and hasattr(ex.fault.detail.ApiFaultDetail.OperationErrors, 'OperationError'):
        api_errors=ex.fault.detail.ApiFaultDetail.OperationErrors.OperationError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'EditorialApiFaultDetail') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail, 'BatchErrors') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail.BatchErrors, 'BatchError'):
        api_errors=ex.fault.detail.EditorialApiFaultDetail.BatchErrors.BatchError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'EditorialApiFaultDetail') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail, 'EditorialErrors') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail.EditorialErrors, 'EditorialError'):
        api_errors=ex.fault.detail.EditorialApiFaultDetail.EditorialErrors.EditorialError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'EditorialApiFaultDetail') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail, 'OperationErrors') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail.OperationErrors, 'OperationError'):
        api_errors=ex.fault.detail.EditorialApiFaultDetail.OperationErrors.OperationError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    # Handle serialization errors e.g. The formatter threw an exception while trying to deserialize the message: 
    # There was an error while trying to deserialize parameter https://bingads.microsoft.com/CampaignManagement/v9:Entities.
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ExceptionDetail'):
        api_errors=ex.fault.detail.ExceptionDetail
        if type(api_errors) == list:
            for api_error in api_errors:
                output_status_message(api_error.Message)
        else:
            output_status_message(api_errors.Message)
    else:
        raise Exception('Unknown WebFault')

def output_client_links(client_links):
    if hasattr(client_links, 'ClientLink'):
        for client_link in client_links['ClientLink']:
            output_status_message("Status: {0}".format(client_link.Status))
            output_status_message("ClientAccountId: {0}".format(client_link.ClientAccountId))
            output_status_message("ClientAccountNumber: {0}".format(client_link.ClientAccountNumber))
            output_status_message("ManagingAgencyCustomerId: {0}".format(client_link.ManagingCustomerId))
            output_status_message("ManagingCustomerNumber: {0}".format(client_link.ManagingCustomerNumber))
            output_status_message("IsBillToClient: True" if client_link.IsBillToClient else "IsBillToClient: False")
            output_status_message("InviterEmail: {0}".format(client_link.InviterEmail))
            output_status_message("InviterName: {0}".format(client_link.InviterName))
            output_status_message("InviterPhone: {0}".format(client_link.InviterPhone))
            output_status_message("LastModifiedByUserId: {0}".format(client_link.LastModifiedByUserId))
            output_status_message("LastModifiedDateTime: {0}".format(client_link.LastModifiedDateTime))
            output_status_message("Name: {0}".format(client_link.Name))
            output_status_message("Note: {0}".format(client_link.Note))
            output_status_message('')

def output_partial_errors(operation_errors, partial_errors):
    if hasattr(operation_errors, 'OperationError'):
        for error in operation_errors['OperationError']:
            output_status_message("OperationError");
            output_status_message("Code: {0}\nMessage: {1}\n".format(error.Code, error.Message))

    if hasattr(partial_errors, 'ArrayOfOperationError'):
        for errors in partial_errors['ArrayOfOperationError']:
            if errors is not None:
                for error in errors['OperationError']:
                    if error is not None:
                        output_status_message("OperationError");
                        output_status_message("Code: {0}\nMessage: {1}\n".format(error.Code, error.Message))

# Main execution
if __name__ == '__main__':

    try:
        authenticate_with_oauth() # To expedite testing

        # Set to an empty user identifier to get the current authenticated Bing Ads user,
        # and then search for all accounts the user may access.
        user=customer_service.GetUser(None).User
        accounts=search_accounts_by_user_id(user.Id)

        # Required in this example for adding new client links
        authorization_data.customer_id=accounts['Account'][0].ParentCustomerId

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
                output_partial_errors(
                    update_client_links_response.OperationErrors,
                    update_client_links_response.PartialErrors
            )

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

            output_partial_errors(add_client_links_response.OperationErrors, add_client_links_response.PartialErrors)
            output_status_message("The user attempted to add a new ClientLink.\n")
            output_status_message("Login as the client Super Admin to accept the agency's request to manage AccountId {0}.\n".format(CLIENT_ACCOUNT_ID))
        
        # Get and print the current client link

        client_links=customer_service.SearchClientLinks(
            Ordering=ordering,
            PageInfo=page_info,
            Predicates=predicates
        )

        output_client_links(client_links)

        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

