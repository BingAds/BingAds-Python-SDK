from bingads import *

import sys
import webbrowser
from time import gmtime, strftime
from datetime import datetime, timedelta
from suds import WebFault

# Optionally you can include logging to output traffic, for example the SOAP request and response.

#import logging
#logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)

if __name__ == '__main__':
    print("Python loads the web service proxies at runtime, so you will observe " \
          "a performance delay between program launch and main execution...\n")

    # Specify the email address where the invitation should be sent. 
    # It is important to note that the recipient can accept the invitation 
    # and sign into Bing Ads with a Microsoft account different than the invitation email address.
    user_invite_recipient_email = "<UserInviteRecipientEmailGoesHere>"

    DEVELOPER_TOKEN='DeveloperTokenGoesHere'
    ENVIRONMENT='production'
    
    # If you are using OAuth in production, CLIENT_ID is required and CLIENT_STATE is recommended.
    CLIENT_ID='ClientIdGoesHere'
    CLIENT_STATE='ClientStateGoesHere'

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
    #return None # To switch users for testing.
    file=None
    try:
        file = open("refresh.txt")
        line = file.readline()
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
   
    paging = {
        'Index': 0,
        'Size': 10
    }

    predicates = {
        'Predicate': [
            {
                'Field': 'UserId',
                'Operator': 'Equals',
                'Value': user_id,
            },
        ]
    }
        
    return customer_service.SearchAccounts(
        PageInfo = paging,
        Predicates = predicates
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
        api_errors = ex.fault.detail.ApiFault.OperationErrors.OperationError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'AdApiFaultDetail') \
        and hasattr(ex.fault.detail.AdApiFaultDetail, 'Errors') \
        and hasattr(ex.fault.detail.AdApiFaultDetail.Errors, 'AdApiError'):
        api_errors = ex.fault.detail.AdApiFaultDetail.Errors.AdApiError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ApiFaultDetail') \
        and hasattr(ex.fault.detail.ApiFaultDetail, 'BatchErrors') \
        and hasattr(ex.fault.detail.ApiFaultDetail.BatchErrors, 'BatchError'):
        api_errors = ex.fault.detail.ApiFaultDetail.BatchErrors.BatchError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ApiFaultDetail') \
        and hasattr(ex.fault.detail.ApiFaultDetail, 'OperationErrors') \
        and hasattr(ex.fault.detail.ApiFaultDetail.OperationErrors, 'OperationError'):
        api_errors = ex.fault.detail.ApiFaultDetail.OperationErrors.OperationError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'EditorialApiFaultDetail') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail, 'BatchErrors') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail.BatchErrors, 'BatchError'):
        api_errors = ex.fault.detail.EditorialApiFaultDetail.BatchErrors.BatchError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'EditorialApiFaultDetail') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail, 'EditorialErrors') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail.EditorialErrors, 'EditorialError'):
        api_errors = ex.fault.detail.EditorialApiFaultDetail.EditorialErrors.EditorialError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'EditorialApiFaultDetail') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail, 'OperationErrors') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail.OperationErrors, 'OperationError'):
        api_errors = ex.fault.detail.EditorialApiFaultDetail.OperationErrors.OperationError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    # Handle serialization errors e.g. The formatter threw an exception while trying to deserialize the message: 
    # There was an error while trying to deserialize parameter https://bingads.microsoft.com/CampaignManagement/v9:Entities.
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ExceptionDetail'):
        api_errors = ex.fault.detail.ExceptionDetail
        if type(api_errors) == list:
            for api_error in api_errors:
                output_status_message(api_error.Message)
        else:
            output_status_message(api_errors.Message)
    else:
        raise Exception('Unknown WebFault')

def output_user_invitations(user_invitations):
    if user_invitations is None:
        return

    for user_invitation in user_invitations:
        output_status_message("FirstName: {0}".format(user_invitation.FirstName))
        output_status_message("LastName: {0}".format(user_invitation.LastName))
        output_status_message("Email: {0}".format(user_invitation.Email))
        output_status_message("Role: {0}".format(user_invitation.Role))
        output_status_message("Invitation Id: {0}\n".format(user_invitation.Id))

def output_user(user):
    if user is None:
        return

    for user_invitation in user_invitations:
        output_status_message("Id: {0}".format(user.Id))
        output_status_message("UserName: {0}".format(user.UserName))
        output_status_message("Contact Email: {0}".format(user.ContactInfo.Email))
        output_status_message("First Name: {0}".format(user.Name.FirstName))
        output_status_message("Last Name: {0}\n".format(user.Name.LastName))

# Main execution
if __name__ == '__main__':
    
    try:
        # You should authenticate for Bing Ads production services with a Microsoft Account, 
        # instead of providing the Bing Ads username and password set. 
        # Authentication with a Microsoft Account is currently not supported in Sandbox.
        authenticate_with_oauth()

        # Uncomment to run with Bing Ads legacy UserName and Password credentials.
        # For example you would use this method to authenticate in sandbox.
        #authenticate_with_username()
        
        # Set to an empty user identifier to get the current authenticated Bing Ads user,
        # and then search for all accounts the user may access.
        user=customer_service.GetUser(None).User
        accounts=search_accounts_by_user_id(user.Id)

        # For this example we'll use the first account.
        authorization_data.account_id=accounts['Account'][0].Id
        authorization_data.customer_id=accounts['Account'][0].ParentCustomerId

        output_status_message("You must edit this example to provide the email address (user_invite_recipient_email) for " \
                              "the user invitation.")
        output_status_message("Login as a Super Admin user to send a user invitation.\n")

        # Prepare to invite a new user
        user_invitation = customer_service.factory.create('ns5:UserInvitation')

        # The identifier of the customer this user is invited to manage. 
        # The AccountIds element determines which customer accounts the user can manage.
        user_invitation.CustomerId = authorization_data.customer_id

        # Users with account level roles such as Advertiser Campaign Manager can be restricted to specific accounts. 
        # Users with customer level roles such as Super Admin can access all accounts within the user’s customer, 
        # and their access cannot be restricted to specific accounts.
        user_invitation.AccountIds=None

         #The user role, which determines the level of access that the user has to the accounts specified in the AccountIds element.
        user_invitation.Role = 'AdvertiserCampaignManager'

        # The email address where the invitation should be sent. This element can contain a maximum of 100 characters.
        user_invitation.Email = user_invite_recipient_email

        # The first name of the user. This element can contain a maximum of 40 characters.
        user_invitation.FirstName = "FirstNameGoesHere"

        # The last name of the user. This element can contain a maximum of 40 characters.
        user_invitation.LastName = "LastNameGoesHere"

        # The locale to use when sending correspondence to the user by email or postal mail. The default is EnglishUS.
        user_invitation.Lcid = 'EnglishUS'

       
        # Once you send a user invitation, there is no option to rescind the invitation using the API.
        # You can delete a pending invitation in the Accounts & Billing -> Users tab of the Bing Ads web application. 
        user_invitation_id=customer_service.SendUserInvitation(user_invitation)
        output_status_message("Sent new user invitation to {0}.\n".format(user_invite_recipient_email))

        # It is possible to have multiple pending invitations sent to the same email address, 
        # which have not yet expired. It is also possible for those invitations to have specified 
        # different user roles, for example if you sent an invitation with an incorrect user role 
        # and then sent a second invitation with the correct user role. The recipient can accept 
        # any of the invitations. The Bing Ads API does not support any operations to delete 
        # pending user invitations. After you invite a user, the only way to cancel the invitation 
        # is through the Bing Ads web application. You can find both pending and accepted invitations 
        # in the Users section of Accounts & Billing.

        # Since a recipient can accept the invitation and sign into Bing Ads with a Microsoft account different 
        # than the invitation email address, you cannot determine with certainty the mapping from UserInvitation 
        # to accepted User. You can search by the invitation ID (returned by SendUserInvitations), 
        # only to the extent of finding out whether or not the invitation has been accepted or has expired. 
        # The SearchUserInvitations operation returns all pending invitations, whether or not they have expired. 
        # Accepted invitations are not included in the SearchUserInvitations response.  

        # This example searches for all user invitations of the customer that you manage,
        # and then filters the search results to find the invitation sent above.
        # Note: In this example the invitation (sent above) should be active and not expired. You can set a breakpoint 
        # and then either accept or delete the invitation in the Bing Ads web application to change the invitation status.

        predicates = {
            'Predicate': [
                {
                    'Field': 'CustomerId',
                    'Operator': 'In',
                    'Value': authorization_data.customer_id,
                },
            ]
        }

        user_invitations = customer_service.SearchUserInvitations(
            Predicates = predicates
        )['UserInvitation']
        output_status_message("Existing UserInvitation(s):\n")
        output_user_invitations(user_invitations)

        # Determine whether the invitation has been accepted or has expired.
        # If you specified a valid InvitationId, and if the invitation is not found, 
        # then the recipient has accepted the invitation. 
        # If the invitation is found, and if the expiration date is later than the current date and time,
        # then the invitation is still pending and has not yet expired. 
        pending_invitation=next((invitation for invitation in user_invitations if 
                                 (invitation.Id == user_invitation_id and invitation.ExpirationDate - datetime.utcnow() > timedelta(seconds=0))
                                 ), "None")

        # You can send a new invitation if the invitation was either not found, has expired, 
        # or the user has accepted the invitation. This example does not send a new invitation if the 
        # invitationId was found and has not yet expired, i.e. the invitation is pending.
        if pending_invitation is None or pending_invitation == 'None':
            # Once you send a user invitation, there is no option to rescind the invitation using the API.
            # You can delete a pending invitation in the Accounts & Billing -> Users tab of the Bing Ads web application. 
            user_invitation_id=customer_service.SendUserInvitation(user_invitation)
            output_status_message("Sent new user invitation to {0}.\n".format(user_invite_recipient_email))
        
        else:
            output_status_message("UserInvitationId {0} is pending.\n".format(user_invitation_id))

        # After the invitation has been accepted, you can call GetUsersInfo and GetUser to access the Bing Ads user details. 
        # Once again though, since a recipient can accept the invitation and sign into Bing Ads with a Microsoft account 
        # different than the invitation email address, you cannot determine with certainty the mapping from UserInvitation 
        # to accepted User. With the user ID returned by GetUsersInfo or GetUser, you can call DeleteUser to remove the user.

        users_info = customer_service.GetUsersInfo(CustomerId=authorization_data.customer_id)['UserInfo']
        confirmed_user_info=next((info for info in users_info if info.UserName == user_invite_recipient_email), "None")
        
        # If the user already accepted, you can call GetUser to view all user details.
        if confirmed_user_info is not None and confirmed_user_info != 'None':
            get_user_response=customer_service.GetUser(confirmed_user_info.Id)
            output_status_message("Found Requested User Details (Not necessarily related to above Invitation ID(s):")
            output_user(get_user_response.User)
            output_status_message("Role Ids:")
            output_status_message("; ".join(str(role) for role in get_user_response.Roles['int']) + "\n")
            
            # You have the option of calling DeleteUser to revoke their access to your customer accounts.
            # Note: Only a super admin or aggregator user can delete users.
            #time_stamp = customer_service.GetUser(confirmed_user_info.Id)['User'].TimeStamp
            #customer_service.DeleteUser(
            #    UserId=confirmed_user_info.Id,
            #    TimeStamp=time_stamp
            #)
            #output_status_message("Deleted UserName {0}.\n".format(user_invite_recipient_email))
        
        output_status_message("Program execution completed")
    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

