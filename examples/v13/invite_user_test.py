from auth_helper import *
from openapi_client.models.customer import *

# You must edit this example to provide the email address of the user you want to invite.
USER_INVITATION_EMAIL = "jayw.92@gmail.com"  # Set this to a valid email address

def main(authorization_data):
    try:
        # 1. Invite a user
        print("-----\nInviteUser:")
        
        invitation = UserInvitation(
            FirstName='FirstNameGoesHere',
            LastName='LastNameGoesHere',
            Email=USER_INVITATION_EMAIL,
            CustomerId=authorization_data.customer_id,
            RoleId=16,  # Set a valid role ID if required
            Lcid='EnglishUS'  # English
        )
        
        invite_request = SendUserInvitationRequest(
            UserInvitation=invitation
        )
        
        invite_response = customer_service.send_user_invitation(invite_request)
        
        print("InviteUserResponse:")
        print(f"User Invitation ID: {invite_response.UserInvitationId}")
        
        assert invite_response is not None
        assert invite_response.UserInvitationId is not None
        
        print(f"User invitation sent successfully to: {USER_INVITATION_EMAIL}")
        
        # 2. Search for user invitations
        print("\n-----\nSearchUserInvitations:")
        
        predicate = Predicate(
            Field='CustomerId',
            Operator='In',
            Value=str(authorization_data.customer_id)
        )
        
        search_request = SearchUserInvitationsRequest(
            Predicates=[predicate]
        )
        
        search_response = customer_service.search_user_invitations(search_request)
        
        print("SearchUserInvitationsResponse:")
        assert search_response is not None
        assert search_response.UserInvitations is not None
        
        print(f"Found {len(search_response.UserInvitations)} user invitations:")
        assert len(search_response.UserInvitations) > 0
        
        for invitation in search_response.UserInvitations:
            print(f"\nFound User Invitation:")
            print(f"  ID: {invitation.Id}")
            print(f"  Email: {invitation.Email}")
            print(f"  FirstName: {invitation.FirstName}")
            print(f"  LastName: {invitation.LastName}")
            print(f"  CustomerId: {invitation.CustomerId}")
            print(f"  RoleId: {invitation.RoleId}")
        
    except Exception as ex:
        print(f"Error occurred: {str(ex)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("Loading the web service client...")
    
    authorization_data = AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )
    
    authenticate(authorization_data)
    
    customer_service = ServiceClient(
        service='CustomerManagementService',
        version=13,
        authorization_data=authorization_data,
        environment=ENVIRONMENT,
    )
    
    main(authorization_data)