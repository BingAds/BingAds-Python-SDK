from bingads import *
from bingads.bulk import *

import sys
import webbrowser
from time import gmtime, strftime

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

    TARGET_ID_KEY=-1
    CAMPAIGN_ID_KEY=-123

    FILE_DIRECTORY='c:/bulk/'
    RESULT_FILE_NAME='download.csv'
    UPLOAD_FILE_NAME='upload.csv'

    authorization_data=AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    # Take advantage of the BulkServiceManager class to efficiently manage ads and keywords for all campaigns in an account. 
    # The client library provides classes to accelerate productivity for downloading and uploading entities. 
    # For example the upload_entities method of the BulkServiceManager class submits your upload request to the bulk service, 
    # polls the service until the upload completed, downloads the result file to a temporary directory, and exposes BulkEntity-derived objects  
    # that contain close representations of the corresponding Campaign Management data objects and value sets.

    # Poll for downloads at reasonable intervals. You know your data better than anyone. 
    # If you download an account that is well less than one million keywords, consider polling 
    # at 15 to 20 second intervals. If the account contains about one million keywords, consider polling 
    # at one minute intervals after waiting five minutes. For accounts with about four million keywords, 
    # consider polling at one minute intervals after waiting 10 minutes. 
      
    bulk_service=BulkServiceManager(
        authorization_data=authorization_data, 
        poll_interval_in_milliseconds=5000, 
        environment=ENVIRONMENT,
    )

    campaign_service=ServiceClient(
        service='CampaignManagementService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )

    customer_service=ServiceClient(
        'CustomerManagementService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
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
    #authorization_data.authentication.token_refreshed_callback=save_refresh_token
    
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
        PageInfo = paging,
        Predicates = predicates
    )

def print_percent_complete(progress):
    output_status_message("Percent Complete: {0}\n".format(progress.percent_complete))

    
def get_sample_bulk_campaign():
    bulk_campaign=BulkCampaign()
    '''
    The client_id may be used to associate records in the bulk upload file with records in the results file. The value of this field  
    is not used or stored by the server; it is simply copied from the uploaded record to the corresponding result record. 
	Note: This bulk file Client Id is not related to an application Client Id for OAuth. 
	'''
    bulk_campaign.client_id='YourClientIdGoesHere'
    campaign=campaign_service.factory.create('Campaign')
    '''
    When using the Campaign Management service, the Id cannot be set. In the context of a BulkCampaign, the Id is optional  
    and may be used as a negative reference key during bulk upload. For example the same negative reference key for the campaign Id  
	will be used when adding new ad groups to this new campaign, or when associating ad extensions with the campaign. 
	'''
    campaign.Id=CAMPAIGN_ID_KEY
    campaign.Name='Winter Clothing ' + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    campaign.Description='Winter clothing line.'
    campaign.BudgetType='MonthlyBudgetSpendUntilDepleted'
    campaign.MonthlyBudget=1000
    campaign.TimeZone='PacificTimeUSCanadaTijuana'
    campaign.Status='Paused'
    bulk_campaign.campaign=campaign

    return bulk_campaign

def get_sample_bulk_campaign_day_time_target():
    bulk_campaign_day_time_target=BulkCampaignDayTimeTarget()
    bulk_campaign_day_time_target.campaign_id=CAMPAIGN_ID_KEY
    bulk_campaign_day_time_target.target_id=TARGET_ID_KEY
    day_time_target=campaign_service.factory.create('DayTimeTarget')
    
    day_time_target_bid_0=campaign_service.factory.create('DayTimeTargetBid')
    day_time_target_bid_0.BidAdjustment=10
    day_time_target_bid_0.Day='Friday'
    day_time_target_bid_0.FromHour=11
    day_time_target_bid_0.FromMinute='Zero'
    day_time_target_bid_0.ToHour=13
    day_time_target_bid_0.ToMinute='Fifteen'

    day_time_target_bid_1=campaign_service.factory.create('DayTimeTargetBid')
    day_time_target_bid_1.BidAdjustment=20
    day_time_target_bid_1.Day='Saturday'
    day_time_target_bid_1.FromHour=11
    day_time_target_bid_1.FromMinute='Zero'
    day_time_target_bid_1.ToHour=13
    day_time_target_bid_1.ToMinute='Fifteen'

    day_time_target.Bids.DayTimeTargetBid.append(day_time_target_bid_0)
    day_time_target.Bids.DayTimeTargetBid.append(day_time_target_bid_1)

    bulk_campaign_day_time_target.day_time_target=day_time_target

    return bulk_campaign_day_time_target

def get_sample_bulk_campaign_location_target():
    bulk_campaign_location_target=BulkCampaignLocationTarget()
    bulk_campaign_location_target.campaign_id=CAMPAIGN_ID_KEY
    bulk_campaign_location_target.target_id=TARGET_ID_KEY

    city_target=campaign_service.factory.create('CityTarget')
    city_target_bid=campaign_service.factory.create('CityTargetBid')
    city_target_bid.BidAdjustment=10
    city_target_bid.City="Toronto, Toronto ON CA"
    city_target_bid.IsExcluded=False
    city_target.Bids.CityTargetBid.append(city_target_bid)
    
    country_target=campaign_service.factory.create('CountryTarget')
    country_target_bid=campaign_service.factory.create('CountryTargetBid')
    country_target_bid.BidAdjustment=15
    country_target_bid.CountryAndRegion="CA"
    country_target_bid.IsExcluded=False
    country_target.Bids.CountryTargetBid.append(country_target_bid)
    
    metro_area_target=campaign_service.factory.create('MetroAreaTarget')
    metro_area_target_bid=campaign_service.factory.create('MetroAreaTargetBid')
    metro_area_target_bid.BidAdjustment=15
    metro_area_target_bid.MetroArea="Seattle-Tacoma, WA, WA US"
    metro_area_target_bid.IsExcluded=False
    metro_area_target.Bids.MetroAreaTargetBid.append(metro_area_target_bid)

    postal_code_target=campaign_service.factory.create('PostalCodeTarget')
    postal_code_target_bid=campaign_service.factory.create('PostalCodeTargetBid')
    postal_code_target_bid.BidAdjustment=15
    postal_code_target_bid.PostalCode="98052, WA US"
    postal_code_target_bid.IsExcluded=False
    postal_code_target.Bids.PostalCodeTargetBid.append(postal_code_target_bid)

    state_target=campaign_service.factory.create('StateTarget')
    state_target_bid=campaign_service.factory.create('StateTargetBid')
    state_target_bid.BidAdjustment=15
    state_target_bid.State="US-WA"
    state_target_bid.IsExcluded=False
    state_target.Bids.StateTargetBid.append(state_target_bid)

    location_target2=campaign_service.factory.create('LocationTarget2')
    location_target2.IntentOption='PeopleIn'
    location_target2.CityTarget=city_target
    location_target2.CountryTarget=country_target
    location_target2.MetroAreaTarget=metro_area_target
    location_target2.PostalCodeTarget=postal_code_target
    location_target2.StateTarget=state_target
    bulk_campaign_location_target.location_target=location_target2
    
    return bulk_campaign_location_target

def get_sample_bulk_campaign_radius_target():
    bulk_campaign_radius_target=BulkCampaignRadiusTarget()
    bulk_campaign_radius_target.campaign_id=CAMPAIGN_ID_KEY
    bulk_campaign_radius_target.target_id=TARGET_ID_KEY
    bulk_campaign_radius_target.intent_option='PeopleInOrSearchingForOrViewingPages'
    BulkAdGroupAgeTarget()
    radius_target2=campaign_service.factory.create('RadiusTarget2')
    radius_target_bid2=campaign_service.factory.create('RadiusTargetBid2')
    radius_target_bid2.BidAdjustment=10
    radius_target_bid2.LatitudeDegrees=47.755367
    radius_target_bid2.LongitudeDegrees=-122.091827
    radius_target_bid2.Radius=11
    radius_target_bid2.RadiusUnit='Kilometers'
    radius_target2.Bids.RadiusTargetBid2.append(radius_target_bid2)
    bulk_campaign_radius_target.radius_target=radius_target2
    
    return bulk_campaign_radius_target

def output_status_message(message):
    print(message)

def output_bulk_campaigns(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaign: \n")
        output_status_message("Campaign Name: {0}".format(entity.campaign.Name))
        output_status_message("Campaign Id: {0}".format(entity.campaign.Id))

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_campaign_day_time_targets(bulk_entities):
    for entity in bulk_entities:
        # If the BulkCampaignDayTimeTarget object was created by the application, and not read from a bulk file, 
        # then there will be no BulkCampaignDayTimeTargetBid objects. For example if you want to print the 
        # BulkCampaignDayTimeTarget prior to upload.
        if len(entity.bids) == 0 and entity.day_time_target is not None:
            output_status_message("BulkCampaignDayTimeTarget: \n")
            output_status_message("Campaign Name: {0}".format(entity.campaign_name))
            output_status_message("Campaign Id: {0}".format(entity.campaign_id))
            output_status_message("Target Id: {0}\n".format(entity.target_id))

            for bid in entity.day_time_target.Bids['DayTimeTargetBid']:
                output_status_message("Campaign Management DayTimeTargetBid Object: ")
                output_status_message("BidAdjustment: {0}".format(bid.BidAdjustment))
                output_status_message("Day: {0}".format(bid.Day))
                output_status_message("From Hour: {0}".format(bid.FromHour))
                output_status_message("From Minute: {0}".format(bid.FromMinute))
                output_status_message("To Hour: {0}".format(bid.ToHour))
                output_status_message("To Minute: {0}".format(bid.ToMinute))
        else:
            output_bulk_campaign_day_time_target_bids(entity.bids)

        output_status_message('')

def output_bulk_campaign_day_time_target_bids(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignDayTimeTargetBid: \n")
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("Campaign Id: {0}".format(entity.campaign_id))
        output_status_message("Target Id: {0}\n".format(entity.target_id))

        output_status_message("Campaign Management DayTimeTargetBid Object: ")
        output_status_message("BidAdjustment: {0}".format(entity.day_time_target_bid.BidAdjustment))
        output_status_message("Day: {0}".format(entity.day_time_target_bid.Day))
        output_status_message("From Hour: {0}".format(entity.day_time_target_bid.FromHour))
        output_status_message("From Minute: {0}".format(entity.day_time_target_bid.FromMinute))
        output_status_message("To Hour: {0}".format(entity.day_time_target_bid.ToHour))
        output_status_message("To Minute: {0}".format(entity.day_time_target_bid.ToMinute))

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_campaign_location_targets(bulk_entities):
    for entity in bulk_entities:
        # If the BulkCampaignLocationTarget object was created by the application, and not read from a bulk file, 
        # then there will be no BulkCampaignLocationTargetBid objects. For example if you want to print the 
        # BulkCampaignLocationTarget prior to upload.
        if len(entity.bids) == 0:
            output_status_message("BulkCampaignLocationTarget: \n")
            output_status_message("Campaign Name: {0}".format(entity.campaign_name))
            output_status_message("Campaign Id: {0}".format(entity.campaign_id))
            output_status_message("Target Id: {0}".format(entity.target_id))
            output_status_message("Intent Option: {0}\n".format(entity.location_target.IntentOption))

            if entity.city_target is not None:
                for bid in entity.city_target.Bids['CityTargetBid']:
                    output_status_message("Campaign Management CityTargetBid Object: ")
                    output_status_message("BidAdjustment: {0}".format(bid.BidAdjustment))
                    output_status_message("City: {0}".format(bid.City))
                    output_status_message("Location Is Excluded: {0}".format(bid.IsExcluded))
            if entity.country_target is not None:
                for bid in entity.country_target.Bids['CountryTargetBid']:
                    output_status_message("Campaign Management CountryTargetBid Object: ")
                    output_status_message("BidAdjustment: {0}".format(bid.BidAdjustment))
                    output_status_message("CountryAndRegion : {0}".format(bid.CountryAndRegion ))
                    output_status_message("Location Is Excluded: {0}".format(bid.IsExcluded))
            if entity.metro_area_target is not None:
                for bid in entity.metro_area_target.Bids['MetroAreaTargetBid']:
                    output_status_message("Campaign Management MetroAreaTargetBid Object: ")
                    output_status_message("BidAdjustment: {0}".format(bid.BidAdjustment))
                    output_status_message("MetroArea: {0}".format(bid.MetroArea))
                    output_status_message("Location Is Excluded: {0}".format(bid.IsExcluded))
            if entity.postal_code_target is not None:
                for bid in entity.postal_code_target.Bids['PostalCodeTargetBid']:
                    output_status_message("Campaign Management PostalCodeTargetBid Object: ")
                    output_status_message("BidAdjustment: {0}".format(bid.BidAdjustment))
                    output_status_message("PostalCode: {0}".format(bid.PostalCode))
                    output_status_message("Location Is Excluded: {0}".format(bid.IsExcluded))
            if entity.state_target is not None:
                for bid in entity.state_target.Bids['StateTargetBid']:
                    output_status_message("Campaign Management StateTargetBid Object: ")
                    output_status_message("BidAdjustment: {0}".format(bid.BidAdjustment))
                    output_status_message("State  : {0}".format(bid.State  ))
                    output_status_message("Location Is Excluded: {0}".format(bid.IsExcluded))
        else:
            output_bulk_campaign_location_target_bids(entity.bids)

        output_status_message('')

def output_bulk_campaign_location_target_bids(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignLocationTargetBid: \n")
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("Campaign Id: {0}".format(entity.campaign_id))
        output_status_message("Target Id: {0}".format(entity.target_id))
        output_status_message("Intent Option: {0}\n".format(entity.intent_option))

        output_status_message("BidAdjustment: {0}".format(entity.bid_adjustment))
        output_status_message("LocationType: {0}".format(entity.location_type))
        output_status_message("Location : {0}".format(entity.location))

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_campaign_radius_targets(bulk_entities):
    for entity in bulk_entities:
        # If the BulkCampaignRadiusTarget object was created by the application, and not read from a bulk file, 
        # then there will be no BulkCampaignRadiusTargetBid objects. For example if you want to print the 
        # BulkCampaignRadiusTarget prior to upload.
        if len(entity.bids) == 0 and entity.radius_target is not None:
            output_status_message("BulkCampaignRadiusTarget: \n")
            output_status_message("Campaign Name: {0}".format(entity.campaign_name))
            output_status_message("Campaign Id: {0}".format(entity.campaign_id))
            output_status_message("Target Id: {0}".format(entity.target_id))
            output_status_message("Intent Option: {0}\n".format(entity.intent_option))

            for bid in entity.radius_target.Bids['RadiusTargetBid2']:
                output_status_message("Campaign Management RadiusTargetBid2 Object: ")
                output_status_message("BidAdjustment: {0}".format(bid.BidAdjustment))
                output_status_message("LatitudeDegrees: {0}".format(bid.LatitudeDegrees))
                output_status_message("LongitudeDegrees: {0}".format(bid.LongitudeDegrees))
                output_status_message("Radius: {0}".format(bid.Radius))
                output_status_message("Radius Unit: {0}".format(bid.RadiusUnit))
        else:
            output_bulk_campaign_radius_target_bids(entity.bids)

        output_status_message('')

def output_bulk_campaign_radius_target_bids(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignRadiusTargetBid: \n")
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("Campaign Id: {0}".format(entity.campaign_id))
        output_status_message("Target Id: {0}".format(entity.target_id))
        output_status_message("Intent Option: {0}\n".format(entity.intent_option))

        output_status_message("Campaign Management RadiusTargetBid Object: ")
        output_status_message("BidAdjustment: {0}".format(entity.radius_target_bid.BidAdjustment))
        output_status_message("LatitudeDegrees: {0}".format(entity.radius_target_bid.LatitudeDegrees))
        output_status_message("LongitudeDegrees: {0}".format(entity.radius_target_bid.LongitudeDegrees))
        output_status_message("Radius: {0}".format(entity.radius_target_bid.Radius))
        output_status_message("RadiusUnit: {0}".format(entity.radius_target_bid.RadiusUnit))

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_errors(errors):
    for error in errors:
        if error.error is not None:
            output_status_message("Number: {0}".format(error.error))
        output_status_message("Error: {0}".format(error.number))
        if error.editorial_reason_code is not None:
            output_status_message("EditorialTerm: {0}".format(error.editorial_term))
            output_status_message("EditorialReasonCode: {0}".format(error.editorial_reason_code))
            output_status_message("EditorialLocation: {0}".format(error.editorial_location))
            output_status_message("PublisherCountries: {0}".format(error.publisher_countries))
        output_status_message('')

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

# Main execution
if __name__ == '__main__':

    errors=[]

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

        # Prepare the bulk entities that you want to upload. Each bulk entity contains the corresponding campaign management object,  
        # and additional elements needed to read from and write to a bulk file.

        bulk_campaign=get_sample_bulk_campaign()
        bulk_campaign_day_time_target=get_sample_bulk_campaign_day_time_target()
        bulk_campaign_location_target=get_sample_bulk_campaign_location_target()
        bulk_campaign_radius_target=get_sample_bulk_campaign_radius_target()

        output_bulk_campaign_day_time_targets([bulk_campaign_day_time_target])
        output_bulk_campaign_location_targets([bulk_campaign_location_target])
        output_bulk_campaign_radius_targets([bulk_campaign_radius_target])
        
        # Write the entities created above, to temporary memory. 
        # Dependent entities such as BulkCampaignLocationTarget must be written after any dependencies,   
        # for example the BulkCampaign. 

        upload_entities=[]
        upload_entities.append(bulk_campaign)
        upload_entities.append(bulk_campaign_day_time_target)
        upload_entities.append(bulk_campaign_location_target)
        upload_entities.append(bulk_campaign_radius_target)
        
        entity_upload_parameters=EntityUploadParameters(
            result_file_directory=FILE_DIRECTORY,
            result_file_name=RESULT_FILE_NAME,
            entities=upload_entities,
            overwrite_result_file=True,
            response_mode='ErrorsAndResults'
        )

        # upload_entities will upload the entities you prepared and will download the results file 
        # Alternative is to write to file and then upload the file. Use upload_file for large uploads.

        output_status_message("Starting upload_entities . . .")

        bulk_entities=bulk_service.upload_entities(entity_upload_parameters, progress=print_percent_complete)

        output_status_message("Printing the results of upload_entities . . .")

        for entity in bulk_entities:
            if isinstance(entity, BulkCampaign):
                output_bulk_campaigns([entity])
            if isinstance(entity, BulkCampaignDayTimeTarget):
                output_bulk_campaign_day_time_targets([entity])
            if isinstance(entity, BulkCampaignLocationTarget):
                output_bulk_campaign_location_targets([entity])
            if isinstance(entity, BulkCampaignRadiusTarget):
                output_bulk_campaign_radius_targets([entity])
            
        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

