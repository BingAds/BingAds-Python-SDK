from auth_helper import *
from customermanagement_example_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    try:
        # Set to an empty user identifier to get the current authenticated Bing Ads user,
        # and then confirm whether the user has aggregator role.
        get_user_response=customer_service.GetUser(UserId=None)
        user = get_user_response.User

        # Only a user with the aggregator role (33) can sign up new customers. 
        # If the user does not have the aggregator role, then do not continue.
        role_ids=[]
        for customer_role in get_user_response.CustomerRoles['CustomerRole']:
            role_ids.append(customer_role.RoleId)
        if(not 33 in role_ids):
            output_status_message("Only a user with the aggregator role (33) can sign up new customers.")
            exit(0)
        
        customer = customer_service.factory.create('ns5:Customer')

        # The primary business segment of the customer, for example, automotive, food, or entertainment.
        customer.Industry = 'Other'

        # The primary country where the customer operates. This country will be the 
        # default country for ad groups in the customer's campaigns.
        customer.MarketCountry = 'US'

        # The primary language that the customer uses. This language will be the 
        # default language for ad groups in the customer's campaigns.
        customer.MarketLanguage = 'English'

        # The name of the customer. This element can contain a maximum of 100 characters.
        customer.Name = "Child Customer " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

        # SUDS requires that you set unused value sets to None
        customer.CustomerFinancialStatus=None
        customer.ServiceLevel=None
        customer.CustomerLifeCycleStatus=None
        
        account=customer_service.factory.create('ns5:AdvertiserAccount')
        
        # The location where your business is legally registered. 
        # The business address is used to determine your tax requirements.
        business_address = customer_service.factory.create('ns5:Address')
        business_address.City = "Redmond"
        business_address.Line1 = "One Microsoft Way"
        business_address.CountryCode = "US"
        business_address.PostalCode = "98052"
        business_address.StateOrProvince = "WA"
        account.BusinessAddress = business_address

        # The type of currency that is used to settle the account. The service uses the currency information for billing purposes.
        account.CurrencyCode = 'USD'

        # Optionally you can set up each account with auto tagging.
        # The AutoTag key and value pair is an account level setting that determines whether to append or replace 
        # the supported UTM tracking codes within the final URL of ads delivered. The default value is 'Inactive' and
        # Bing Ads will not append any UTM tracking codes to your ad or keyword final URL.
        account.AutoTagType='Inactive'

        # The name of the account. The name can contain a maximum of 100 characters and must be unique within the customer.
        account.Name = "Child Account " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

        # The identifier of the customer that owns the account. In the Bing Ads API operations 
        # that require a customer identifier, this is the identifier that you set the CustomerId SOAP header to.
        account.ParentCustomerId = user.CustomerId

        # The TaxInformation (e.g. VAT number) is optional. If specified, The VAT number must be valid 
        # in the country that you specified in the BusinessAddress element. Without a VAT registration 
        # number or exemption certificate, taxes might apply based on your business location.
        account.TaxInformation = None

        # The time-zone value to use for campaigns in this account.
        account.TimeZone = 'PacificTimeUSCanadaTijuana'

        # SUDS requires that you set unused value sets to None
        account.AccountFinancialStatus=None
        account.Language=None
        account.PaymentMethodType=None
        account.AccountLifeCycleStatus=None
    
        # Signup a new customer and account for the reseller. 
        signup_customer_response =  customer_service.SignupCustomer(
            customer,
            account,
            user.CustomerId)

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
        version=12,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )

    # You should authenticate for Bing Ads production services with a Microsoft Account.
        
    authenticate(authorization_data)
        
    main(authorization_data)
