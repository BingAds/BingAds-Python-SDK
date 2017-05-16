from datetime import datetime, timedelta

from auth_helper import *
from output_helper import *

# You must provide credentials in auth_helper.py.

# Specify the email address where the invitation should be sent. 
# It is important to note that the recipient can accept the invitation 
# and sign into Bing Ads with a Microsoft account different than the invitation email address.
INVITE_EMAIL_TO = "UserInviteRecipientEmailGoesHere"

def main(authorization_data):
    
    try:
        output_status_message("You must edit this example to provide the email address (e.g. {0}) for " \
                              "the user invitation.".format(INVITE_EMAIL_TO))
        output_status_message("Login as a Super Admin user to send a user invitation.\n")

        # Prepare to invite a new user
        user_invitation = customer_service.factory.create('ns5:UserInvitation')

        # The identifier of the customer this user is invited to manage. 
        # The AccountIds element determines which customer accounts the user can manage.
        user_invitation.CustomerId = authorization_data.customer_id

        # Users with account level roles such as Advertiser Campaign Manager can be restricted to specific accounts. 
        # Users with customer level roles such as Super Admin can access all accounts within the user's customer, 
        # and their access cannot be restricted to specific accounts.
        user_invitation.AccountIds=None

         #The user role, which determines the level of access that the user has to the accounts specified in the AccountIds element.
        user_invitation.Role = 'AdvertiserCampaignManager'

        # The email address where the invitation should be sent. This element can contain a maximum of 100 characters.
        user_invitation.Email = INVITE_EMAIL_TO

        # The first name of the user. This element can contain a maximum of 40 characters.
        user_invitation.FirstName = "FirstNameGoesHere"

        # The last name of the user. This element can contain a maximum of 40 characters.
        user_invitation.LastName = "LastNameGoesHere"

        # The locale to use when sending correspondence to the user by email or postal mail. The default is EnglishUS.
        user_invitation.Lcid = 'EnglishUS'

       
        # Once you send a user invitation, there is no option to rescind the invitation using the API.
        # You can delete a pending invitation in the Accounts & Billing -> Users tab of the Bing Ads web application. 
        user_invitation_id=customer_service.SendUserInvitation(user_invitation)
        output_status_message("Sent new user invitation to {0}.\n".format(INVITE_EMAIL_TO))

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
            output_status_message("Sent new user invitation to {0}.\n".format(INVITE_EMAIL_TO))
        
        else:
            output_status_message("UserInvitationId {0} is pending.\n".format(user_invitation_id))

        # After the invitation has been accepted, you can call GetUsersInfo and GetUser to access the Bing Ads user details. 
        # Once again though, since a recipient can accept the invitation and sign into Bing Ads with a Microsoft account 
        # different than the invitation email address, you cannot determine with certainty the mapping from UserInvitation 
        # to accepted User. With the user ID returned by GetUsersInfo or GetUser, you can call DeleteUser to remove the user.

        users_info = customer_service.GetUsersInfo(CustomerId=authorization_data.customer_id)['UserInfo']
        confirmed_user_info=next((info for info in users_info if info.UserName == INVITE_EMAIL_TO), "None")
        
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
            #output_status_message("Deleted UserName {0}.\n".format(INVITE_EMAIL_TO))
        
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
        'CustomerManagementService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=11,
    )

    # You should authenticate for Bing Ads production services with a Microsoft Account, 
    # instead of providing the Bing Ads username and password set. 
    # Authentication with a Microsoft Account is currently not supported in Sandbox.
        
    authenticate(authorization_data)
        
    main(authorization_data)