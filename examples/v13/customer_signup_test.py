from auth_helper import *
from openapi_client.models.customer import *


def main(authorization_data):
    try:
        # 1. Get user and verify aggregator role
        print("-----\nGetUser:")
        get_user_request = GetUserRequest(
            UserId=None
        )
        
        user_response = customer_service.get_user(get_user_request)
        user = user_response.User
        
        print("GetUserResponse:")
        print(f"User: {user}")
        assert user is not None
        assert user.CustomerId is not None
        
        print("Checking if user has aggregator role...")
        role_ids = [role.RoleId for role in user_response.CustomerRoles]
        print(f"User Roles: {', '.join(map(str, role_ids))}")
        
        if 33 not in role_ids:
            raise Exception("Only a user with the aggregator role (33) can sign up new customers.")
        
        print("User has aggregator role, proceeding with signup...")
        
        # 2. Sign up a new customer
        print("\n-----\nSignupCustomer:")
        
        # Create customer
        customer = Customer(
            Name=f'Child Customer {str(uuid.uuid4())[:8]}',
            Industry='Other',
            MarketCountry='US',
            MarketLanguage='English'
        )
        
        # Create account with business address
        business_address = Address(
            City='Redmond',
            CountryCode='US',
            PostalCode='98052',
            StateOrProvince='WA',
            Line1='One Microsoft Way'
        )
        
        account = AdvertiserAccount(
            BusinessAddress=business_address,
            CurrencyCode='USDollar',
            Name=f'Child Account {str(uuid.uuid4())[:8]}',
            ParentCustomerId=user.CustomerId,
            TaxInformation=None,
            TimeZone='PacificTimeUSCanadaTijuana'
        )
        
        signup_request = SignupCustomerRequest(
            Customer=customer,
            Account=account,
            ParentCustomerId=user.CustomerId
        )
        
        signup_response = customer_service.signup_customer(signup_request)
        
        print("SignupCustomerResponse:")
        print(f"Customer ID: {signup_response.CustomerId}")
        print(f"Account ID: {signup_response.AccountId}")
        print(f"Customer Number: {signup_response.CustomerNumber}")
        print(f"Account Number: {signup_response.AccountNumber}")
        
        assert signup_response.CustomerId is not None
        assert signup_response.AccountId is not None
        assert signup_response.AccountNumber is not None
        assert signup_response.CustomerNumber is not None
        
        print(f"\nNew Customer ID: {signup_response.CustomerId}")
        print(f"New Account ID: {signup_response.AccountId}")
        print(f"New Customer Number: {signup_response.CustomerNumber}")
        print(f"New Account Number: {signup_response.AccountNumber}")
        
    except Exception as ex:
        print(f"Error occurred: {str(ex)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    import uuid
    
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