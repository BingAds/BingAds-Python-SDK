from datetime import datetime, timedelta

from auth_helper import *
from customermanagement_example_helper import *

# You must provide credentials in auth_helper.py.

# Specify the email address where the invitation should be sent. 
# The recipient can accept the invitation and sign up 
# with credentials that differ from the invitation email address.
INVITE_EMAIL_TO = "UserInviteRecipientEmailGoesHere"

def main(authorization_data):
    
    try:
        output_status_message("You must edit this example to provide the email address (e.g. {0}) for " \
                              "the user invitation.".format(INVITE_EMAIL_TO))
        output_status_message("Login as a Super Admin user to send a user invitation.")

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
        #For example you can use Role Id 16 for Advertiser Campaign Manager. 
        user_invitation.RoleId = 16

        # The email address where the invitation should be sent. 
        user_invitation.Email = INVITE_EMAIL_TO

        # The first name of the user. 
        user_invitation.FirstName = "FirstNameGoesHere"

        # The last name of the user. 
        user_invitation.LastName = "LastNameGoesHere"

        # The locale to use when sending correspondence to the user by email or postal mail. The default is EnglishUS.
        user_invitation.Lcid = 'EnglishUS'
       
        # Once you send a user invitation, there is no option to rescind the invitation using the API.
        # You can delete a pending invitation in the Accounts & Billing -> Users tab of the Bing Ads web application. 

        output_status_message("-----\nSendUserInvitation:")
        user_invitation_id=customer_service.SendUserInvitation(
            UserInvitation=user_invitation)
        output_status_message("Sent new user invitation to {0}.".format(INVITE_EMAIL_TO))
        output_status_message("UserInvitationId: {0}".format(user_invitation_id))

        # It is possible to have multiple pending invitations sent to the same email address, 
        # which have not yet expired. It is also possible for those invitations to have specified 
        # different user roles, for example if you sent an invitation with an incorrect user role 
        # and then sent a second invitation with the correct user role. The recipient can accept 
        # any of the invitations. The Bing Ads API does not support any operations to delete 
        # pending user invitations. After you invite a user, the only way to cancel the invitation 
        # is through the Bing Ads web application. You can find both pending and accepted invitations 
        # in the Users section of Accounts & Billing.

        # Since a recipient can accept the invitation with credentials that differ from 
        # the invitation email address, you cannot determine with certainty the mapping from UserInvitation 
        # to accepted User. You can only determine whether the invitation has been accepted or has expired. 
        # The SearchUserInvitations operation returns all pending invitations, whether or not they have expired. 
        # Accepted invitations are not included in the SearchUserInvitations response.  

        predicates = {
            'Predicate': [
                {
                    'Field': 'CustomerId',
                    'Operator': 'In',
                    'Value': authorization_data.customer_id,
                },
            ]
        }

        output_status_message("-----\nSearchUserInvitations:")
        user_invitations = customer_service.SearchUserInvitations(
            Predicates = predicates
        )
        output_status_message("UserInvitations:")
        output_array_of_userinvitation(user_invitations)       

        # After the invitation has been accepted, you can call GetUsersInfo and GetUser to access the Bing Ads user details. 
        # Once again though, since a recipient can accept the invitation with credentials that differ from 
        # the invitation email address, you cannot determine with certainty the mapping from UserInvitation 
        # to accepted User. 

        output_status_message("-----\nGetUsersInfo:")
        users_info = customer_service.GetUsersInfo(
            CustomerId=authorization_data.customer_id,
            StatusFilter=None)
        output_status_message("UsersInfo:")
        output_array_of_userinfo(users_info)

        for info in users_info['UserInfo']:            
            output_status_message("-----\nGetUser:")
            get_user_response=customer_service.GetUser(
                UserId=info.Id,
                IncludeLinkedAccountIds=True)
            user = get_user_response.User
            customer_roles=get_user_response.CustomerRoles
            output_status_message("User:")
            output_user(user)
            output_status_message("CustomerRoles:")
            output_array_of_customerrole(customer_roles)
    
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
        version=13,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )
        
    authenticate(authorization_data)
        
    main(authorization_data)
