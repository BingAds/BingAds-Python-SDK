from bingads import *

import sys
import webbrowser
from time import gmtime, strftime
from suds import WebFault

# Optionally you can include logging to output traffic, for example the SOAP request and response.

import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

if __name__ == '__main__':
    print("Python loads the web service proxies at runtime, so you will observe " \
          "a performance delay between program launch and main execution...\n")

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

    search_accounts_request = {
        'PageInfo': paging,
        'Predicates': predicates
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
        get_user_response=customer_service.GetUser(UserId=None)
        user = get_user_response.User
               
        # Only a user with the aggregator role (33) can sign up new customers. 
        # If the user does not have the aggregator role, then do not continue.
        if(not 33 in get_user_response.Roles['int']):
            output_status_message("Only a user with the aggregator role (33) can sign up new customers.");
            exit(0)

        # For Customer.CustomerAddress and Account.BusinessAddress, you can use the same address 
        # as your aggregator user, although you must set Id and TimeStamp to null.
        user_address = user.ContactInfo.Address
        user_address.Id = None
        user_address.TimeStamp = None
        
        customer = customer_service.factory.create('ns5:Customer')

        # The customer's business address.
        customer.CustomerAddress = user_address

        # The list of key and value strings for forward compatibility. This element can be used
        # to avoid otherwise breaking changes when new elements are added in future releases.
        # There are currently no forward compatibility changes for the Customer object.
        customer.ForwardCompatibilityMap = None

        # The primary business segment of the customer, for example, automotive, food, or entertainment.
        customer.Industry = 'Other'

        # The primary country where the customer operates. This country will be the 
        # default country for ad groups in the customer�s campaigns.
        customer.MarketCountry = 'US'

        # The primary language that the customer uses. This language will be the 
        # default language for ad groups in the customer�s campaigns.
        customer.MarketLanguage = 'English'

        # The name of the customer. This element can contain a maximum of 100 characters.
        customer.Name = "Child Customer " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

        # SUDS requires that you set unused value sets to None
        customer.CustomerFinancialStatus=None
        customer.ServiceLevel=None
        customer.CustomerLifeCycleStatus=None
        
        account=customer_service.factory.create('ns5:AdvertiserAccount')
                
        # The type of account. Bing Ads API only supports the Advertiser account.
        account.AccountType = 'Advertiser'

        # The location where your business is legally registered. 
        # The business address is used to determine your tax requirements.
        # BusinessAddress will be required in a future version of the Bing Ads API.
        # Please start using it.
        account.BusinessAddress = user_address

        # The type of currency that is used to settle the account. The service uses the currency information for billing purposes.
        account.CurrencyType = 'USDollar'

        # Optionally you can set up each account with auto tagging.
        # The AutoTag key and value pair is an account level setting that determines whether to append or replace 
        # the supported UTM tracking codes within the final URL of ads delivered. The default value is '0', and
        # Bing Ads will not append any UTM tracking codes to your ad or keyword final URL.
        account_FCM = customer_service.factory.create('ns0:ArrayOfKeyValuePairOfstringstring')
        auto_tag=customer_service.factory.create('ns0:KeyValuePairOfstringstring')
        auto_tag.key="AutoTag"
        auto_tag.value="0"
        account_FCM.KeyValuePairOfstringstring.append(auto_tag)
        
        # The list of key and value strings for forward compatibility. This element can be used
        # to avoid otherwise breaking changes when new elements are added in future releases.
        account.ForwardCompatibilityMap = account_FCM

        # The name of the account. The name can contain a maximum of 100 characters and must be unique within the customer.
        account.Name = "Child Account " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

        # The identifier of the customer that owns the account. In the Bing Ads API operations 
        # that require a customer identifier, this is the identifier that you set the CustomerId SOAP header to.
        account.ParentCustomerId = user.CustomerId

        # The TaxId (VAT identifier) is optional. If specified, The VAT identifier must be valid 
        #in the country that you specified in the BusinessAddress element. Without a VAT registration 
        # number or exemption certificate, taxes might apply based on your business location.
        account.TaxId = None

        # The default time-zone value to use for campaigns in this account.
        # If not specified, the time zone will be set to PacificTimeUSCanadaTijuana by default.
        # TimeZone will be required in a future version of the Bing Ads API.
        # Please start using it. 
        account.TimeZone = 'PacificTimeUSCanadaTijuana'

        # SUDS requires that you set unused value sets to None
        account.AccountFinancialStatus=None
        account.Language=None
        account.PaymentMethodType=None
        account.AccountLifeCycleStatus=None
        account.TaxType=None
        account.TaxIdStatus=None
    
        # Signup a new customer and account for the reseller. 
        signup_customer_response =  customer_service.SignupCustomer(
            customer,
            account,
            user.CustomerId);

        output_status_message("New Customer and Account:\n")

        # This is the identifier that you will use to set the CustomerId 
        # element in most of the Bing Ads API service operations.
        output_status_message("\tCustomerId: {0}".format(signup_customer_response.CustomerId))

        # The read-only system-generated customer number that is used in the Bing Ads web application. 
        # The customer number is of the form, Cnnnnnnn, where nnnnnnn is a series of digits.
        output_status_message("\tCustomerNumber: {0}".format(signup_customer_response.CustomerNumber))

        # This is the identifier that you will use to set the AccountId and CustomerAccountId 
        # elements in most of the Bing Ads API service operations.
        output_status_message("\tAccountId: {0}".format(signup_customer_response.AccountId))

        # The read-only system generated account number that is used to identify the account in the Bing Ads web application. 
        # The account number has the form xxxxxxxx, where xxxxxxxx is a series of any eight alphanumeric characters.
        output_status_message("\tAccountNumber: {0}\n".format(signup_customer_response.AccountNumber))

        output_status_message("Program execution completed")
    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

