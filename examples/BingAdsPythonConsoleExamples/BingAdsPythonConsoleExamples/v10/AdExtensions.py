from bingads.service_client import ServiceClient
from bingads.authorization import *
from bingads.v10 import *

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

    campaign_service=ServiceClient(
        service='CampaignManagementService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=10,
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
    # There was an error while trying to deserialize parameter https://bingads.microsoft.com/CampaignManagement/v10:Entities.
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
        
def set_elements_to_none(suds_object):
    # Bing Ads Campaign Management service operations require that if you specify a non-primitives, 
    # it must be one of the values defined by the service i.e. it cannot be a nil element. 
    # Since Suds requires non-primitives and Bing Ads won't accept nil elements in place of an enum value, 
    # you must either set the non-primitives or they must be set to None. Also in case new properties are added 
    # in a future service release, it is a good practice to set each element of the SUDS object to None as a baseline. 

    for (element) in suds_object:
        suds_object.__setitem__(element[0], None)
    return suds_object

def output_campaign_ids(campaign_ids):
    for id in campaign_ids['long']:
        output_status_message("Campaign successfully added and assigned CampaignId {0}\n".format(id))

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
                output_app_ad_extension(extension)
            elif extension.Type == 'CallAdExtension':
                output_call_ad_extension(extension)
            elif extension.Type == 'CalloutAdExtension':
                output_callout_ad_extension(extension)
            elif extension.Type == 'LocationAdExtension':
                output_location_ad_extension(extension)
            elif extension.Type == 'ReviewAdExtension':
                output_review_ad_extension(extension)
            elif extension.Type == 'SiteLinksAdExtension':
                output_site_links_ad_extension(extension)
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

def output_app_ad_extension(extension):
    if extension is not None:
        output_status_message("Id: {0}".format(extension.Id))
        output_status_message("Type: {0}".format(extension.Type))
        output_status_message("AppPlatform: {0}".format(extension.AppPlatform))
        output_status_message("AppStoreId: {0}".format(extension.AppStoreId))
        output_status_message("DestinationUrl: {0}".format(extension.DestinationUrl))
        output_status_message("DevicePreference: {0}".format(extension.DevicePreference))
        output_status_message("DisplayText: {0}".format(extension.DisplayText))
        output_status_message("Status: {0}".format(extension.Status))
        output_status_message("Version: {0}".format(extension.Version))
        output_status_message('')

def output_call_ad_extension(extension):
    if extension is not None:
        output_status_message("Id: {0}".format(extension.Id))
        output_status_message("Type: {0}".format(extension.Type))
        output_status_message("CountryCode: {0}".format(extension.CountryCode))
        output_status_message("DevicePreference: {0}".format(extension.DevicePreference))
        output_status_message("IsCallOnly: {0}".format(extension.IsCallOnly))
        output_status_message("IsCallTrackingEnabled: {0}".format(extension.IsCallTrackingEnabled))
        output_status_message("PhoneNumber: {0}".format(extension.PhoneNumber))
        output_status_message("RequireTollFreeTrackingNumber: {0}".format(extension.RequireTollFreeTrackingNumber))
        output_status_message("Status: {0}".format(extension.Status))
        output_status_message("Version: {0}".format(extension.Version))
        output_status_message('')

def output_callout_ad_extension(extension):
    if extension is not None:
        output_status_message("Id: {0}".format(extension.Id))
        output_status_message("Type: {0}".format(extension.Type))
        output_status_message("Callout Text: {0}".format(extension.Text))
        output_status_message("Status: {0}".format(extension.Status))
        output_status_message("Version: {0}".format(extension.Version))
        output_status_message('')

def output_location_ad_extension(extension):
    if extension is not None:
        output_status_message("Id: {0}".format(extension.Id))
        output_status_message("Type: {0}".format(extension.Type))
        if extension.Address is not None:
            output_status_message("CityName: {0}".format(extension.Address.CityName))
            output_status_message("CountryCode: {0}".format(extension.Address.CountryCode))
            output_status_message("PostalCode: {0}".format(extension.Address.PostalCode))
            output_status_message("ProvinceCode: {0}".format(extension.Address.ProvinceCode))
            output_status_message("ProvinceName: {0}".format(extension.Address.ProvinceName))
            output_status_message("StreetAddress: {0}".format(extension.Address.StreetAddress))
            output_status_message("StreetAddress2: {0}".format(extension.Address.StreetAddress2))
        output_status_message("CompanyName: {0}".format(extension.CompanyName))
        output_status_message("GeoCodeStatus: {0}".format(extension.GeoCodeStatus))
        if extension.GeoPoint is not None:
            output_status_message("GeoPoint: ")
            output_status_message("LatitudeInMicroDegrees: {0}".format(extension.GeoPoint.LatitudeInMicroDegrees))
            output_status_message("LongitudeInMicroDegrees: {0}".format(extension.GeoPoint.LongitudeInMicroDegrees))
        output_status_message("IconMediaId: {0}".format(extension.IconMediaId))
        output_status_message("ImageMediaId: {0}".format(extension.ImageMediaId))
        output_status_message("PhoneNumber: {0}".format(extension.PhoneNumber))
        output_status_message("Status: {0}".format(extension.Status))
        output_status_message("Version: {0}".format(extension.Version))
        output_status_message('')

def output_review_ad_extension(extension):
    if extension is not None:
        output_status_message("Id: {0}".format(extension.Id))
        output_status_message("Type: {0}".format(extension.Type))
        output_status_message("IsExact: {0}".format(extension.IsExact))
        output_status_message("Source: {0}".format(extension.Source))
        output_status_message("Text: {0}".format(extension.Text))
        output_status_message("Url: {0}".format(extension.Url))
        output_status_message("Status: {0}".format(extension.Status))
        output_status_message("Version: {0}".format(extension.Version))
        output_status_message('')

def output_site_links_ad_extension(extension):
    if extension is not None:
        output_status_message("Id: {0}".format(extension.Id))
        output_status_message("Type: {0}".format(extension.Type))
        output_status_message("Status: {0}".format(extension.Status))
        output_status_message("Version: {0}".format(extension.Version))
        output_site_links(extension.SiteLinks)
        output_status_message('')

def output_site_links(site_links):
    if site_links is not None:
        for site_link in site_links['SiteLink']:
            output_status_message("Description1: {0}".format(site_link.Description1))
            output_status_message("Description2: {0}".format(site_link.Description2))
            output_status_message("DevicePreference: {0}".format(site_link.DevicePreference))
            output_status_message("DisplayText: {0}".format(site_link.DisplayText))
            output_status_message("DestinationUrl: {0}".format(site_link.DestinationUrl))
            output_status_message("FinalMobileUrls: ")
            if site_link.FinalMobileUrls is not None:
                for final_mobile_url in site_link.FinalMobileUrls['string']:
                    output_status_message("\t{0}".format(final_mobile_url))
            output_status_message("FinalUrls: ")
            if site_link.FinalUrls is not None:
                for final_url in site_link.FinalUrls['string']:
                    output_status_message("\t{0}".format(final_url))
            output_status_message("TrackingUrlTemplate: {0}".format(site_link.TrackingUrlTemplate))
            output_status_message("UrlCustomParameters: ")
            if site_link.UrlCustomParameters is not None and site_link.UrlCustomParameters.Parameters is not None:
                for custom_parameter in site_link.UrlCustomParameters.Parameters['CustomParameter']:
                    output_status_message("\tKey: {0}".format(custom_parameter.Key))
                    output_status_message("\tValue: {0}".format(custom_parameter.Value))
            output_status_message('')

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
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.Name="Summer Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description="Summer shoes line."
        campaign.BudgetType='MonthlyBudgetSpendUntilDepleted'
        campaign.MonthlyBudget=1000
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.DaylightSaving='true' # Accepts 'true', 'false', True, or False
        campaign.Status='Paused'

        # Used with FinalUrls shown in the sitelinks that we will add below.
        campaign.TrackingUrlTemplate="http://tracker.example.com/?season={_season}&promocode={_promocode}&u={lpurl}"

        campaigns.Campaign.append(campaign)

        add_campaigns_response=campaign_service.AddCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=campaigns
        )
        campaign_ids={
            'long': add_campaigns_response.CampaignIds['long'] if add_campaigns_response.CampaignIds['long'] else None
        }

        output_campaign_ids(campaign_ids)
        
        # Specify the extensions.

        ad_extensions=campaign_service.factory.create('ArrayOfAdExtension')
        
        app_ad_extension=set_elements_to_none(campaign_service.factory.create('AppAdExtension'))
        app_ad_extension.AppPlatform='Windows'
        app_ad_extension.AppStoreId='AppStoreIdGoesHere'
        app_ad_extension.DisplayText='Contoso'
        app_ad_extension.DestinationUrl='DestinationUrlGoesHere'
        # If you supply the AppAdExtension properties above, then you can add this line.
        #ad_extensions.AdExtension.append(app_ad_extension)

        call_ad_extension=set_elements_to_none(campaign_service.factory.create('CallAdExtension'))
        call_ad_extension.CountryCode="US"
        call_ad_extension.PhoneNumber="2065550100"
        call_ad_extension.IsCallOnly=False
        call_ad_extension.Status=None
        ad_extensions.AdExtension.append(call_ad_extension)

        callout_ad_extension=set_elements_to_none(campaign_service.factory.create('CalloutAdExtension'))
        callout_ad_extension.Text="Callout Text"
        ad_extensions.AdExtension.append(callout_ad_extension)

        location_ad_extension=set_elements_to_none(campaign_service.factory.create('LocationAdExtension'))
        location_ad_extension.PhoneNumber="206-555-0100"
        location_ad_extension.CompanyName="Contoso Shoes"
        address=campaign_service.factory.create('Address')
        address.StreetAddress="1234 Washington Place"
        address.StreetAddress2="Suite 1210"
        address.CityName="Woodinville"
        address.ProvinceName="WA"
        address.CountryCode="US"
        address.PostalCode="98608"
        location_ad_extension.Address=address
        ad_extensions.AdExtension.append(location_ad_extension)

        review_ad_extension=set_elements_to_none(campaign_service.factory.create('ReviewAdExtension'))
        review_ad_extension.IsExact=True
        review_ad_extension.Source="Review Source Name"
        review_ad_extension.Text="Review Text"
        review_ad_extension.Url="http://review.contoso.com" # The Url of the third-party review. This is not your business Url.
        ad_extensions.AdExtension.append(review_ad_extension)
        
        site_links_ad_extension=set_elements_to_none(campaign_service.factory.create('SiteLinksAdExtension'))
        site_links=campaign_service.factory.create('ArrayOfSiteLink')

        for index in range(2):
            site_link=set_elements_to_none(campaign_service.factory.create('SiteLink'))
            site_link.DisplayText = "Women's Shoe Sale " + str(index)

            # If you are currently using the Destination URL, you must upgrade to Final URLs. 
            # Here is an example of a DestinationUrl you might have used previously. 
            # site_link.DestinationUrl='http://www.contoso.com/womenshoesale/?season=spring&promocode=PROMO123'

            # To migrate from DestinationUrl to FinalUrls for existing sitelinks, you can set DestinationUrl
            # to an empty string when updating the sitelink. If you are removing DestinationUrl,
            # then FinalUrls is required.
            # site_link.DestinationUrl=""
            
            # With FinalUrls you can separate the tracking template, custom parameters, and 
            # landing page URLs.
            final_urls=campaign_service.factory.create('ns4:ArrayOfstring')
            final_urls.string.append('http://www.contoso.com/womenshoesale')
            site_link.FinalUrls=final_urls

            # Final Mobile URLs can also be used if you want to direct the user to a different page 
            # for mobile devices.
            final_mobile_urls=campaign_service.factory.create('ns4:ArrayOfstring')
            final_mobile_urls.string.append('http://mobile.contoso.com/womenshoesale')
            site_link.FinalMobileUrls=final_mobile_urls

            # You could use a tracking template which would override the campaign level
            # tracking template. Tracking templates defined for lower level entities 
            # override those set for higher level entities.
            # In this example we are using the campaign level tracking template.
            site_link.TrackingUrlTemplate=None

            # Set custom parameters that are specific to this sitelink, 
            # and can be used by the sitelink, ad group, campaign, or account level tracking template. 
            # In this example we are using the campaign level tracking template.
            url_custom_parameters=campaign_service.factory.create('ns0:CustomParameters')
            parameters=campaign_service.factory.create('ns0:ArrayOfCustomParameter')
            custom_parameter1=campaign_service.factory.create('ns0:CustomParameter')
            custom_parameter1.Key='promoCode'
            custom_parameter1.Value='PROMO' + str(index)
            parameters.CustomParameter.append(custom_parameter1)
            custom_parameter2=campaign_service.factory.create('ns0:CustomParameter')
            custom_parameter2.Key='season'
            custom_parameter2.Value='summer'
            parameters.CustomParameter.append(custom_parameter2)
            url_custom_parameters.Parameters=parameters
            site_link.UrlCustomParameters=url_custom_parameters
            site_links.SiteLink.append(site_link)

        site_links_ad_extension.SiteLinks=site_links
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
            ad_extension_id_to_entity_id_association.EntityId=campaign_ids['long'][0]
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

        ad_extensions_type_filter='AppAdExtension CallAdExtension CalloutAdExtension LocationAdExtension ReviewAdExtension SiteLinksAdExtension'
        
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

        campaign_service.DeleteCampaigns(
            AccountId=authorization_data.account_id,
            CampaignIds=campaign_ids
        )

        for campaign_id in campaign_ids['long']:
            output_status_message("Deleted CampaignId {0}\n".format(campaign_id))

        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

