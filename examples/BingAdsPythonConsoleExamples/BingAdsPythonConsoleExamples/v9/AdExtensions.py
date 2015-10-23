from bingads import *

import sys
import webbrowser
from time import gmtime, strftime
from suds import WebFault

# Optionally you can include logging to output traffic, for example the SOAP request and response.

#import logging
#logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)

if __name__ == '__main__':
    print("Python loads the web service proxies at runtime, so you will observe " \
          "a performance delay between program launch and main execution...\n")

    ENVIRONMENT='production'
    DEVELOPER_TOKEN='YourDeveloperTokenGoesHere'
    CLIENT_ID='YourClientIdGoesHere'

    authorization_data=AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    campaign_service=ServiceClient(
        service='CampaignManagementService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=9,
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

    # Assign this authentication instance to the global authorization_data. 
    authorization_data.authentication=authentication   

    # Register the callback function to automatically save the refresh token anytime it is refreshed.
    # Uncomment this line if you want to store your refresh token. Be sure to save your refresh token securely.
    authorization_data.authentication.token_refreshed_callback=save_refresh_token
    
    refresh_token=get_refresh_token()
    
    # If we have a refresh token let's refresh it
    if refresh_token is not None:
        authentication.request_oauth_tokens_by_refresh_token(refresh_token)
    else:
        webbrowser.open(authentication.get_authorization_endpoint(), new=1)
        # For Python 3.x use 'input' instead of 'raw_input'
        if(sys.version_info.major >= 3):
            response_uri=input(
                "You need to provide consent for the application to access your Bing Ads accounts. " \
                "After you have granted consent in the web browser for the application to access your Bing Ads accounts, " \
                "please enter the response URI that includes the authorization 'code' parameter: \n"
            )
        else:
            response_uri=raw_input(
                "You need to provide consent for the application to access your Bing Ads accounts. " \
                "After you have granted consent in the web browser for the application to access your Bing Ads accounts, " \
                "please enter the response URI that includes the authorization 'code' parameter: \n"
            )

        # Request access and refresh tokens using the URI that you provided manually during program execution.
        authentication.request_oauth_tokens_by_response_uri(response_uri=response_uri) 

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
        PageInfo=paging,
        Predicates=predicates
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

def output_ad_extensions(ad_extensions, ad_extension_editorial_reason_collection):
    if not hasattr(ad_extensions, 'AdExtension'):
        return None
    index=0
    for extension in ad_extensions['AdExtension']:
        if extension is None or extension.Id is None:
            output_status_message('Extension is empty or invalid.')
        else:
            output_status_message("Ad extension ID: {0}".format(extension.Id))
            output_status_message("Ad extension Type: {0}".format(extension.Type))

            if extension.Type == 'AppAdExtension':
                output_status_message("AppPlatform: {0}".format(extension.AppPlatform))
                output_status_message("AppStoreId: {0}".format(extension.AppStoreId))
                output_status_message("DestinationUrl: {0}".format(extension.DestinationUrl))
                output_status_message("DevicePreference: {0}".format(extension.DevicePreference))
                output_status_message("DisplayText: {0}".format(extension.DisplayText))
                output_status_message("Id: {0}".format(extension.Id))
                output_status_message("Status: {0}".format(extension.Status))
                output_status_message("Version: {0}".format(extension.Version))
                output_status_message("\n")
            elif extension.Type == 'CallAdExtension':
                output_status_message("Phone number: {0}".format(extension.PhoneNumber))
                output_status_message("Country: {0}".format(extension.CountryCode))
                output_status_message("Is only clickable item: {0}".format(extension.IsCallOnly))
                output_status_message("\n")
            elif extension.Type == 'LocationAdExtension':
                output_status_message("Company name: {0}".format(extension.CompanyName))
                output_status_message("Phone number: {0}".format(extension.PhoneNumber))
                output_status_message("Street: {0}".format(extension.Address.StreetAddress))
                output_status_message("City: {0}".format(extension.Address.CityName))
                output_status_message("State: {0}".format(extension.Address.ProvinceName))
                output_status_message("Country: {0}".format(extension.Address.CountryCode))
                output_status_message("Zip code: {0}".format(extension.Address.PostalCode))
                output_status_message("Business coordinates determined?: {0}".format(extension.GeoCodeStatus))
                output_status_message("Map icon ID: {0}".format(extension.IconMediaId))
                output_status_message("Business image ID: {0}".format(extension.ImageMediaId))
                output_status_message("\n")
            elif extension.Type == 'SiteLinksAdExtension':
                for sitelink in extension.SiteLinks['SiteLink']:
                    output_status_message("Display URL: {0}".format(sitelink.DisplayText))
                    output_status_message("Destination URL: {0}".format(sitelink.DestinationUrl))
                    output_status_message("\n")
            else:
                output_status_message("Unknown extension type")

        if hasattr(ad_extension_editorial_reason_collection, 'Reasons'):

            # Print any editorial rejection reasons for the corresponding extension. This example 
            # assumes the same list index for adExtensions and adExtensionEditorialReasonCollection
            # as defined above.

            for ad_extension_editorial_reason \
            in ad_extension_editorial_reason_collection.Reasons['AdExtensionEditorialReason']:
            
                if ad_extension_editorial_reason is not None \
                and ad_extension_editorial_reason.PublisherCountries is not None:

                    output_status_message("Editorial Rejection Location: {0}".format(ad_extension_editorial_reason.Location))
                    output_status_message("Editorial Rejection PublisherCountries: ")
                    for publisher_country in ad_extension_editorial_reason.PublisherCountries['string']:
                        output_status_message("  " + publisher_country)
                    
                    output_status_message("Editorial Rejection ReasonCode: {0}".format(ad_extension_editorial_reason.ReasonCode))
                    output_status_message("Editorial Rejection Term: {0}".format(ad_extension_editorial_reason.Term))
                    output_status_message("\n")
                              
        index=index+1

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

        # Add a campaign that will later be associated with ad extensions. 

        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=campaign_service.factory.create('Campaign')
        campaign.Name="Summer Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description="Summer shoes line."
        campaign.BudgetType='MonthlyBudgetSpendUntilDepleted'
        campaign.MonthlyBudget=1000
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.DaylightSaving='true' # Accepts 'true', 'false', True, or False
        campaign.Status='Paused'
        campaigns.Campaign.append(campaign)

        campaign_ids=campaign_service.AddCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=campaigns
        )['long']
        
        # Specify the extensions.

        ad_extensions=campaign_service.factory.create('ArrayOfAdExtension')
        
        app_ad_extension=campaign_service.factory.create('AppAdExtension')
        app_ad_extension.AppPlatform='Windows'
        app_ad_extension.AppStoreId='AppStoreIdGoesHere'
        app_ad_extension.DisplayText='Contoso'
        app_ad_extension.DestinationUrl='DestinationUrlGoesHere'
        app_ad_extension.Status=None
        ad_extensions.AdExtension.append(app_ad_extension)

        call_ad_extension=campaign_service.factory.create('CallAdExtension')
        call_ad_extension.CountryCode="US"
        call_ad_extension.PhoneNumber="2065550100"
        call_ad_extension.IsCallOnly=False
        call_ad_extension.Status=None
        ad_extensions.AdExtension.append(call_ad_extension)

        location_ad_extension=campaign_service.factory.create('LocationAdExtension')
        location_ad_extension.PhoneNumber="206-555-0100"
        location_ad_extension.CompanyName="Contoso Shoes"
        location_ad_extension.IconMediaId=None
        location_ad_extension.ImageMediaId=None
        location_ad_extension.Status=None
        location_ad_extension.GeoCodeStatus=None
        location_ad_extension.GeoPoint=None
        address=campaign_service.factory.create('Address')
        address.StreetAddress="1234 Washington Place"
        address.StreetAddress2="Suite 1210"
        address.CityName="Woodinville"
        address.ProvinceName="WA"
        address.CountryCode="US"
        address.PostalCode="98608"
        location_ad_extension.Address=address
        ad_extensions.AdExtension.append(location_ad_extension)
        
        site_links_ad_extension=campaign_service.factory.create('SiteLinksAdExtension')
        site_links=campaign_service.factory.create('ArrayOfSiteLink')
        site_link_0=campaign_service.factory.create('SiteLink')
        site_link_0.DestinationUrl = "Contoso.com"
        site_link_0.DisplayText = "Women's Shoe Sale 1"
        site_links.SiteLink.append(site_link_0)
        site_link_1=campaign_service.factory.create('SiteLink')
        site_link_1.DestinationUrl = "Contoso.com/WomenShoeSale/2"
        site_link_1.DisplayText = "Women's Shoe Sale 2"
        site_links.SiteLink.append(site_link_1)
        site_links_ad_extension.SiteLinks=site_links
        site_links_ad_extension.Status=None
        ad_extensions.AdExtension.append(site_links_ad_extension)
        
        # Add all extensions to the account's ad extension library
        ad_extension_identities=campaign_service.AddAdExtensions(
            AccountId=authorization_data.account_id,
            AdExtensions=ad_extensions
        )

        output_status_message("Added ad extensions.\n")

        # DeleteAdExtensionsAssociations, SetAdExtensionsAssociations, and GetAdExtensionsEditorialReasons 
        # operations each require a list of type AdExtensionIdToEntityIdAssociation.
        ad_extension_id_to_entity_id_associations=campaign_service.factory.create('ArrayOfAdExtensionIdToEntityIdAssociation')

        # GetAdExtensionsByIds requires a list of type long.
        ad_extension_ids=[]

        # Loop through the list of extension IDs and build any required data structures
        # for subsequent operations. 

        for ad_extension_identity in ad_extension_identities['AdExtensionIdentity']:
            ad_extension_id_to_entity_id_association=campaign_service.factory.create('AdExtensionIdToEntityIdAssociation')
            ad_extension_id_to_entity_id_association.AdExtensionId=ad_extension_identity.Id
            ad_extension_id_to_entity_id_association.EntityId=campaign_ids[0]
            ad_extension_id_to_entity_id_associations.AdExtensionIdToEntityIdAssociation.append(ad_extension_id_to_entity_id_association)

            ad_extension_ids.append(ad_extension_identity.Id)

        # Associate the specified ad extensions with the respective campaigns or ad groups. 
        campaign_service.SetAdExtensionsAssociations(
            AccountId=authorization_data.account_id,
            AdExtensionIdToEntityIdAssociations=ad_extension_id_to_entity_id_associations,
            AssociationType='Campaign'
        )

        output_status_message("Set ad extension associations.\n")

        # Get editorial rejection reasons for the respective ad extension and entity associations.
        ad_extension_editorial_reason_collection=campaign_service.GetAdExtensionsEditorialReasons(
            AccountId=authorization_data.account_id,
            AdExtensionIdToEntityIdAssociations=ad_extension_id_to_entity_id_associations,
            AssociationType='Campaign'
        )

        ad_extensions_type_filter='AppAdExtension CallAdExtension LocationAdExtension SiteLinksAdExtension'

        # Get the specified ad extensions from the account?s ad extension library.
        ad_extensions=campaign_service.factory.create('ArrayOfAdExtension')
        ad_extensions=campaign_service.GetAdExtensionsByIds(
            AccountId=authorization_data.account_id,
            AdExtensionIds={'long': ad_extension_ids},
            AdExtensionType=ad_extensions_type_filter,
        )

        output_ad_extensions(ad_extensions, ad_extension_editorial_reason_collection)

        # Remove the specified associations from the respective campaigns or ad groups. 
        # The extesions are still available in the account's extensions library. 
        campaign_service.DeleteAdExtensionsAssociations(
            AccountId=authorization_data.account_id,
            AdExtensionIdToEntityIdAssociations=ad_extension_id_to_entity_id_associations,
            AssociationType='Campaign'
        )

        output_status_message("Deleted ad extension associations.\n")

        # Deletes the ad extensions from the account?s ad extension library.
        campaign_service.DeleteAdExtensions(
            AccountId=authorization_data.account_id,
            AdExtensionIds={'long': ad_extension_ids},
        )

        output_status_message("Deleted ad extensions.\n")

        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

