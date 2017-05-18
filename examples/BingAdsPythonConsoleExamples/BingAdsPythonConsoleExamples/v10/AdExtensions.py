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
#logging.getLogger('suds.transport.http').setLevel(logging.DEBUG)

if __name__ == '__main__':
    print("Python loads the web service proxies at runtime, so you will observe " \
          "a performance delay between program launch and main execution...\n")

    DEVELOPER_TOKEN='DeveloperTokenGoesHere'
    ENVIRONMENT='production'

    # If you are using OAuth in production, CLIENT_ID is required and CLIENT_STATE is recommended.
    CLIENT_ID='ClientIdGoesHere'
    CLIENT_STATE='ClientStateGoesHere'

    SITELINK_MIGRATION = 'SiteLinkAdExtension'

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

# Set the read-only properties of an ad extension to null. This operation can be useful between calls to
# GetAdExtensionsByIds and UpdateAdExtensions. The update operation would fail if you send certain read-only
# fields.
def set_read_only_ad_extension_elements_to_none(extension):
    if extension is None or extension.Id is None:
        return extension
    else:
        # Set to None for all extension types.
        extension.Version = None
    
        if extension.Type == 'LocationAdExtension':
            extension.GeoCodeStatus = None
        
        return extension

                        
def output_ad_extensions(ad_extensions, ad_extension_editorial_reason_collection):
    if not hasattr(ad_extensions, 'AdExtension'):
        return None
    index=0
    for extension in ad_extensions['AdExtension']:
        if extension is None or extension.Id is None:
            output_status_message('Extension is empty or invalid.')
        else:
            if extension.Type == 'AppAdExtension':
                output_app_ad_extension(extension)
            elif extension.Type == 'CallAdExtension':
                output_call_ad_extension(extension)
            elif extension.Type == 'CalloutAdExtension':
                output_callout_ad_extension(extension)
            elif extension.Type == 'ImageAdExtension':
                output_image_ad_extension(extension)
            elif extension.Type == 'LocationAdExtension':
                output_location_ad_extension(extension)
            elif extension.Type == 'ReviewAdExtension':
                output_review_ad_extension(extension)
            elif extension.Type == 'SiteLinksAdExtension':
                output_site_links_ad_extension(extension)
            elif extension.Type == 'Sitelink2AdExtension':
                output_sitelink2_ad_extension(extension)
            elif extension.Type == 'StructuredSnippetAdExtension':
                output_structured_snippet_ad_extension(extension)
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
                              
        index=index+1

    output_status_message("\n")

def output_ad_extension(extension):
    if extension is not None:
        output_status_message("Id: {0}".format(extension.Id))
        output_status_message("Type: {0}".format(extension.Type))
        output_status_message("ForwardCompatibilityMap: ")
        if extension.ForwardCompatibilityMap is not None:
            for pair in extension.ForwardCompatibilityMap['KeyValuePairOfstringstring']:
                output_status_message("Key: {0}".format(pair.Key))
                output_status_message("Value: {0}".format(pair.Value))
        output_status_message("Scheduling: ")
        # Scheduling is not emitted by default, so we must first test whether it exists.
        if hasattr(extension, 'Scheduling') and extension.Scheduling is not None:
            output_schedule(extension.Scheduling)
        output_status_message("Status: {0}".format(extension.Status))
        output_status_message("Version: {0}".format(extension.Version))

def output_schedule(schedule):
    if schedule is not None:
        if schedule.DayTimeRanges is not None:
            for day_time in schedule.DayTimeRanges['DayTime']:
                output_status_message("Day: {0}".format(day_time.Day))
                output_status_message("EndHour: {0}".format(day_time.EndHour))
                output_status_message("EndMinute: {0}".format(day_time.EndMinute))
                output_status_message("StartHour: {0}".format(day_time.StartHour))
                output_status_message("StartMinute: {0}".format(day_time.StartMinute))
        if schedule.EndDate is not None:
            output_status_message(("EndDate: {0}/{1}/{2}".format( 
            schedule.EndDate.Month,
            schedule.EndDate.Day,
            schedule.EndDate.Year)))
        if schedule.StartDate is not None:
            output_status_message(("StartDate: {0}/{1}/{2}".format(
            schedule.StartDate.Month,
            schedule.StartDate.Day,
            schedule.StartDate.Year)))
        use_searcher_time_zone = \
            True if (schedule.UseSearcherTimeZone is not None and schedule.UseSearcherTimeZone == True) else False
        output_status_message("UseSearcherTimeZone: {0}".format(use_searcher_time_zone))

def output_app_ad_extension(extension):
    if extension is not None:
        # Output inherited properties of the AdExtension base class.
        output_ad_extension(extension)

        # Output properties that are specific to the AppAdExtension
        output_status_message("AppPlatform: {0}".format(extension.AppPlatform))
        output_status_message("AppStoreId: {0}".format(extension.AppStoreId))
        output_status_message("DestinationUrl: {0}".format(extension.DestinationUrl))
        output_status_message("DevicePreference: {0}".format(extension.DevicePreference))
        output_status_message("DisplayText: {0}".format(extension.DisplayText))

def output_call_ad_extension(extension):
    if extension is not None:
        # Output inherited properties of the AdExtension base class.
        output_ad_extension(extension)

        # Output properties that are specific to the CallAdExtension
        output_status_message("CountryCode: {0}".format(extension.CountryCode))
        output_status_message("DevicePreference: {0}".format(extension.DevicePreference))
        output_status_message("IsCallOnly: {0}".format(extension.IsCallOnly))
        output_status_message("IsCallTrackingEnabled: {0}".format(extension.IsCallTrackingEnabled))
        output_status_message("PhoneNumber: {0}".format(extension.PhoneNumber))
        output_status_message("RequireTollFreeTrackingNumber: {0}".format(extension.RequireTollFreeTrackingNumber))

def output_callout_ad_extension(extension):
    if extension is not None:
        # Output inherited properties of the AdExtension base class.
        output_ad_extension(extension)

        # Output properties that are specific to the CalloutAdExtension
        output_status_message("Callout Text: {0}".format(extension.Text))

def output_image_ad_extension(extension):
    if extension is not None:
        # Output inherited properties of the AdExtension base class.
        output_ad_extension(extension)

        # Output properties that are specific to the ImageAdExtension
        output_status_message("AlternativeText: {0}".format(extension.AlternativeText))
        output_status_message("Description: {0}".format(extension.Description))
        output_status_message("DestinationUrl: {0}".format(extension.DestinationUrl))
        output_status_message("FinalMobileUrls: ")
        if extension.FinalMobileUrls is not None:
            for final_mobile_url in extension.FinalMobileUrls['string']:
                output_status_message("\t{0}".format(final_mobile_url))
        output_status_message("FinalUrls: ")
        if extension.FinalUrls is not None:
            for final_url in extension.FinalUrls['string']:
                output_status_message("\t{0}".format(final_url))
        output_status_message("ImageMediaIds: ")
        if extension.ImageMediaIds is not None:
            for id in extension.ImageMediaIds['string']:
                output_status_message("\t{0}".format(id))
        output_status_message("TrackingUrlTemplate: {0}".format(extension.TrackingUrlTemplate))
        output_status_message("UrlCustomParameters: ")
        if extension.UrlCustomParameters is not None and extension.UrlCustomParameters.Parameters is not None:
            for custom_parameter in extension.UrlCustomParameters.Parameters['CustomParameter']:
                output_status_message("\tKey: {0}".format(custom_parameter.Key))
                output_status_message("\tValue: {0}".format(custom_parameter.Value))

def output_location_ad_extension(extension):
    if extension is not None:
        # Output inherited properties of the AdExtension base class.
        output_ad_extension(extension)

        # Output properties that are specific to the LocationAdExtension
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

def output_review_ad_extension(extension):
    if extension is not None:
        # Output inherited properties of the AdExtension base class.
        output_ad_extension(extension)

        # Output properties that are specific to the ReviewAdExtension
        output_status_message("IsExact: {0}".format(extension.IsExact))
        output_status_message("Source: {0}".format(extension.Source))
        output_status_message("Text: {0}".format(extension.Text))
        output_status_message("Url: {0}".format(extension.Url))

def output_structured_snippet_ad_extension(extension):
    if extension is not None:
        # Output inherited properties of the AdExtension base class.
        output_ad_extension(extension)

        # Output properties that are specific to the StructuredSnippetAdExtension
        output_status_message("Header: {0}".format(extension.Header))
        for value in extension.Values['string']:
            output_status_message("\t{0}".format(value))
        
def output_site_links_ad_extension(extension):
    if extension is not None:
        # Output inherited properties of the AdExtension base class.
        output_ad_extension(extension)

        # Output properties that are specific to the SiteLinksAdExtension
        output_site_links(extension.SiteLinks['SiteLink'])

def output_site_links(site_links):
    if site_links is not None:
        for site_link in site_links:
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
            
def output_sitelink2_ad_extension(extension):
    if extension is not None:
        # Output inherited properties of the AdExtension base class.
        output_ad_extension(extension)

        # Output properties that are specific to the Sitelink2AdExtension
        output_status_message("Description1: {0}".format(extension.Description1))
        output_status_message("Description2: {0}".format(extension.Description2))
        output_status_message("DevicePreference: {0}".format(extension.DevicePreference))
        output_status_message("DisplayText: {0}".format(extension.DisplayText))
        output_status_message("DestinationUrl: {0}".format(extension.DestinationUrl))
        output_status_message("FinalMobileUrls: ")
        if extension.FinalMobileUrls is not None:
            for final_mobile_url in extension.FinalMobileUrls['string']:
                output_status_message("\t{0}".format(final_mobile_url))
        output_status_message("FinalUrls: ")
        if extension.FinalUrls is not None:
            for final_url in extension.FinalUrls['string']:
                output_status_message("\t{0}".format(final_url))
        output_status_message("TrackingUrlTemplate: {0}".format(extension.TrackingUrlTemplate))
        output_status_message("UrlCustomParameters: ")
        if extension.UrlCustomParameters is not None and extension.UrlCustomParameters.Parameters is not None:
            for custom_parameter in extension.UrlCustomParameters.Parameters['CustomParameter']:
                output_status_message("\tKey: {0}".format(custom_parameter.Key))
                output_status_message("\tValue: {0}".format(custom_parameter.Value))

def output_account_migration_statuses_info(account_migration_statuses_info):
    if account_migration_statuses_info is not None:
        output_status_message("AccountId: {0}".format(account_migration_statuses_info.AccountId))
        for migration_status_info in account_migration_statuses_info['MigrationStatusInfo']:
            output_migration_status_info(migration_status_info)
            
def output_migration_status_info(migration_status_info):
    if migration_status_info is not None and migration_status_info[1] is not None:
        output_status_message("MigrationType: {0}".format(migration_status_info[1][0].MigrationType))
        output_status_message("StartTimeInUtc: {0}".format(migration_status_info[1][0].StartTimeInUtc))
        output_status_message("Status: {0}".format(migration_status_info[1][0].Status))

def get_sample_site_links_ad_extensions():
    site_links_ad_extensions=campaign_service.factory.create('ArrayOfAdExtension')
    site_links_ad_extension=set_elements_to_none(campaign_service.factory.create('SiteLinksAdExtension'))
    site_links=campaign_service.factory.create('ArrayOfSiteLink')

    for index in range(2):
        site_link=set_elements_to_none(campaign_service.factory.create('SiteLink'))
        site_link.Description1="Simple & Transparent."
        site_link.Description2="No Upfront Cost."
        site_link.DisplayText = "Women's Shoe Sale " + str(index)

        # If you are currently using the Destination URL, you must upgrade to Final URLs. 
        # Here is an example of a DestinationUrl you might have used previously. 
        # site_link.DestinationUrl='http://www.contoso.com/womenshoesale/?season=spring&promocode=PROMO123'

        # To migrate from DestinationUrl to FinalUrls, you can set DestinationUrl
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
    site_links_ad_extensions.AdExtension.append(site_links_ad_extension)

    return site_links_ad_extensions

def get_sample_sitelink2_ad_extensions():
    sitelink2_ad_extensions=campaign_service.factory.create('ArrayOfAdExtension')
    
    for index in range(2):
        sitelink2_ad_extension=set_elements_to_none(campaign_service.factory.create('Sitelink2AdExtension'))
        sitelink2_ad_extension.Description1="Simple & Transparent."
        sitelink2_ad_extension.Description2="No Upfront Cost."
        sitelink2_ad_extension.DisplayText = "Women's Shoe Sale " + str(index)

        # If you are currently using the Destination URL, you must upgrade to Final URLs. 
        # Here is an example of a DestinationUrl you might have used previously. 
        # sitelink2_ad_extension.DestinationUrl='http://www.contoso.com/womenshoesale/?season=spring&promocode=PROMO123'

        # To migrate from DestinationUrl to FinalUrls, you can set DestinationUrl
        # to an empty string when updating the ad extension. If you are removing DestinationUrl,
        # then FinalUrls is required.
        # sitelink2_ad_extension.DestinationUrl=""
            
        # With FinalUrls you can separate the tracking template, custom parameters, and 
        # landing page URLs.
        final_urls=campaign_service.factory.create('ns4:ArrayOfstring')
        final_urls.string.append('http://www.contoso.com/womenshoesale')
        sitelink2_ad_extension.FinalUrls=final_urls

        # Final Mobile URLs can also be used if you want to direct the user to a different page 
        # for mobile devices.
        final_mobile_urls=campaign_service.factory.create('ns4:ArrayOfstring')
        final_mobile_urls.string.append('http://mobile.contoso.com/womenshoesale')
        sitelink2_ad_extension.FinalMobileUrls=final_mobile_urls

        # You could use a tracking template which would override the campaign level
        # tracking template. Tracking templates defined for lower level entities 
        # override those set for higher level entities.
        # In this example we are using the campaign level tracking template.
        sitelink2_ad_extension.TrackingUrlTemplate=None

        # Set custom parameters that are specific to this ad extension, 
        # and can be used by the ad extension, ad group, campaign, or account level tracking template. 
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
        sitelink2_ad_extension.UrlCustomParameters=url_custom_parameters
        sitelink2_ad_extensions.AdExtension.append(sitelink2_ad_extension)

    return sitelink2_ad_extensions

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


        # To prepare for the sitelink ad extensions migration by the end of September 2017, you will need 
        # to determine whether the account has been migrated from SiteLinksAdExtension to Sitelink2AdExtension. 
        # All ad extension service operations available for both types of sitelinks; however you will 
        # need to determine which type to add, update, and retrieve.

        sitelink_migration_is_completed = False

        # Optionally you can find out which pilot features the customer is able to use. Even if the customer 
        # is in pilot for sitelink migrations, the accounts that it contains might not be migrated.
        feature_pilot_flags = customer_service.GetCustomerPilotFeatures(authorization_data.customer_id)

        # The pilot flag value for Sitelink ad extension migration is 253.
        # Pilot flags apply to all accounts within a given customer; however,
        # each account goes through migration individually and has its own migration status.
        if(253 in feature_pilot_flags['int']):
            # Account migration status below will be either NotStarted, InProgress, or Completed.
            output_status_message("Customer is in pilot for Sitelink migration.\n")
        else:
            # Account migration status below will be NotInPilot.
            output_status_message("Customer is not in pilot for Sitelink migration.\n")
        
        # Even if you have multiple accounts per customer, each account will have its own
        # migration status. This example checks one account using the provided AuthorizationData.
        account_migration_statuses_infos = campaign_service.GetAccountMigrationStatuses(
            {'long': authorization_data.account_id},
            SITELINK_MIGRATION
        )

        for account_migration_statuses_info in account_migration_statuses_infos['AccountMigrationStatusesInfo']:
            output_account_migration_statuses_info(account_migration_statuses_info)
            for migration_status_info in account_migration_statuses_info['MigrationStatusInfo']:
                if migration_status_info[1][0].Status == 'Completed' and SITELINK_MIGRATION == migration_status_info[1][0].MigrationType: 
                    sitelink_migration_is_completed = True

         
        # Add a campaign that will later be associated with ad extensions. 

        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.Name="Summer Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description="Summer shoes line."
        campaign.BudgetType='DailyBudgetStandard'
        campaign.DailyBudget=10
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
        # For this example assume the call center is open Monday - Friday from 9am - 9pm
        # in the account's time zone.
        call_scheduling=set_elements_to_none(campaign_service.factory.create('Schedule'))
        call_day_time_ranges=campaign_service.factory.create('ArrayOfDayTime')
        call_monday=set_elements_to_none(campaign_service.factory.create('DayTime'))
        call_monday.Day='Monday'
        call_monday.StartHour=9
        call_monday.StartMinute='Zero'
        call_monday.EndHour=21
        call_monday.EndMinute='Zero'
        call_day_time_ranges.DayTime.append(call_monday)
        call_tuesday=set_elements_to_none(campaign_service.factory.create('DayTime'))
        call_tuesday.Day='Tuesday'
        call_tuesday.StartHour=9
        call_tuesday.StartMinute='Zero'
        call_tuesday.EndHour=21
        call_tuesday.EndMinute='Zero'
        call_day_time_ranges.DayTime.append(call_tuesday)
        call_wednesday=set_elements_to_none(campaign_service.factory.create('DayTime'))
        call_wednesday.Day='Wednesday'
        call_wednesday.StartHour=9
        call_wednesday.StartMinute='Zero'
        call_wednesday.EndHour=21
        call_wednesday.EndMinute='Zero'
        call_day_time_ranges.DayTime.append(call_wednesday)
        call_thursday=set_elements_to_none(campaign_service.factory.create('DayTime'))
        call_thursday.Day='Thursday'
        call_thursday.StartHour=9
        call_thursday.StartMinute='Zero'
        call_thursday.EndHour=21
        call_thursday.EndMinute='Zero'
        call_day_time_ranges.DayTime.append(call_thursday)
        call_friday=set_elements_to_none(campaign_service.factory.create('DayTime'))
        call_friday.Day='Friday'
        call_friday.StartHour=9
        call_friday.StartMinute='Zero'
        call_friday.EndHour=21
        call_friday.EndMinute='Zero'
        call_day_time_ranges.DayTime.append(call_friday)
        call_scheduling.DayTimeRanges=call_day_time_ranges
        call_scheduling_end_date=campaign_service.factory.create('Date')
        call_scheduling_end_date.Day=31
        call_scheduling_end_date.Month=12
        call_scheduling_end_date.Year=strftime("%Y", gmtime())
        call_scheduling.EndDate=call_scheduling_end_date
        call_scheduling.StartDate=None
        call_ad_extension.Scheduling=call_scheduling
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
        location_scheduling=set_elements_to_none(campaign_service.factory.create('Schedule'))
        location_day_time_ranges=campaign_service.factory.create('ArrayOfDayTime')
        location_day_time=set_elements_to_none(campaign_service.factory.create('DayTime'))
        location_day_time.Day='Saturday'
        location_day_time.StartHour=9
        location_day_time.StartMinute='Zero'
        location_day_time.EndHour=12
        location_day_time.EndMinute='Zero'
        location_day_time_ranges.DayTime.append(location_day_time)
        location_scheduling.DayTimeRanges=location_day_time_ranges
        location_scheduling_end_date=campaign_service.factory.create('Date')
        location_scheduling_end_date.Day=31
        location_scheduling_end_date.Month=12
        location_scheduling_end_date.Year=strftime("%Y", gmtime())
        location_scheduling.EndDate=location_scheduling_end_date
        location_scheduling.StartDate=None
        location_ad_extension.Scheduling=location_scheduling
        ad_extensions.AdExtension.append(location_ad_extension)

        review_ad_extension=set_elements_to_none(campaign_service.factory.create('ReviewAdExtension'))
        review_ad_extension.IsExact=True
        review_ad_extension.Source="Review Source Name"
        review_ad_extension.Text="Review Text"
        review_ad_extension.Url="http://review.contoso.com" # The Url of the third-party review. This is not your business Url.
        ad_extensions.AdExtension.append(review_ad_extension)

        structured_snippet_ad_extension=set_elements_to_none(campaign_service.factory.create('StructuredSnippetAdExtension'))
        structured_snippet_ad_extension.Header = "Brands"
        values=campaign_service.factory.create('ns4:ArrayOfstring')
        values.string.append('Windows')
        values.string.append('Xbox')
        values.string.append('Skype')
        structured_snippet_ad_extension.Values=values
        ad_extensions.AdExtension.append(structured_snippet_ad_extension)
        
        ad_extensions.AdExtension.append(
            get_sample_sitelink2_ad_extensions()['AdExtension'] 
            if sitelink_migration_is_completed 
            else get_sample_site_links_ad_extensions()['AdExtension'])

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

        ad_extensions_type_filter='AppAdExtension ' \
                                  'CallAdExtension ' \
                                  'CalloutAdExtension ' \
                                  'ImageAdExtension ' \
                                  'LocationAdExtension ' \
                                  'ReviewAdExtension ' \
                                  'StructuredSnippetAdExtension'
        
        ad_extensions_type_filter+=(' Sitelink2AdExtension' if sitelink_migration_is_completed else ' SiteLinksAdExtension')
        
        return_additional_fields='Scheduling'

        # Get the specified ad extensions from the account's ad extension library.
        ad_extensions=campaign_service.factory.create('ArrayOfAdExtension')
        ad_extensions=campaign_service.GetAdExtensionsByIds(
            AccountId=authorization_data.account_id,
            AdExtensionIds={'long': ad_extension_ids},
            AdExtensionType=ad_extensions_type_filter,
            ReturnAdditionalFields=return_additional_fields
        )

        output_status_message("List of ad extensions that were added above:\n")
        output_ad_extensions(ad_extensions, ad_extension_editorial_reason_collection)

        # Get only the location extensions and remove scheduling.

        adExtensionsTypeFilter = 'LocationAdExtension'

        ad_extensions=campaign_service.GetAdExtensionsByIds(
            AccountId=authorization_data.account_id,
            AdExtensionIds={'long': ad_extension_ids},
            AdExtensionType=ad_extensions_type_filter,
            ReturnAdditionalFields=return_additional_fields
        )

        update_extensions=campaign_service.factory.create('ArrayOfAdExtension')
        update_extension_ids = []

        for extension in ad_extensions['AdExtension']:

            # GetAdExtensionsByIds will return a nil element if the request filters / conditions were not met.
            if extension is not None and extension.Id is not None:
            
                # Remove read-only elements that would otherwise cause the update operation to fail.
                update_extension = set_read_only_ad_extension_elements_to_none(extension)

                # If you set the Scheduling element null, any existing scheduling set for the ad extension will remain unchanged. 
                # If you set this to any non-null Schedule object, you are effectively replacing existing scheduling 
                # for the ad extension. In this example, we will remove any existing scheduling by setting this element  
                # to an empty Schedule object.
                update_extension.Scheduling=campaign_service.factory.create('Schedule')

                update_extensions.AdExtension.append(update_extension)
                update_extension_ids.append(update_extension.Id)
        
        output_status_message("Removing scheduling from the location ad extensions..\n");
        campaign_service.UpdateAdExtensions(
            AccountId=authorization_data.account_id,
            AdExtensions=update_extensions
        )

        ad_extensions=campaign_service.GetAdExtensionsByIds(
            AccountId=authorization_data.account_id,
            AdExtensionIds={'long': update_extension_ids},
            AdExtensionType=ad_extensions_type_filter,
            ReturnAdditionalFields=return_additional_fields
        )

        output_status_message("List of ad extensions that were updated above:\n");
        output_ad_extensions(ad_extensions, None)


        # Remove the specified associations from the respective campaigns or ad groups. 
        # The extesions are still available in the account's extensions library. 
        campaign_service.DeleteAdExtensionsAssociations(
            AccountId=authorization_data.account_id,
            AdExtensionIdToEntityIdAssociations=ad_extension_id_to_entity_id_associations,
            AssociationType='Campaign'
        )

        output_status_message("Deleted ad extension associations.\n")

        # Deletes the ad extensions from the account's ad extension library.
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

