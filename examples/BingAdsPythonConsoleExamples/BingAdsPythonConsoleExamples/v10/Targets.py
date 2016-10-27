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
    if not hasattr(campaign_ids, 'long'):
        return None
    for id in campaign_ids:
        output_status_message("Campaign successfully added and assigned CampaignId {0}\n".format(id))

def output_ad_group_ids(ad_group_ids):
    if not hasattr(ad_group_ids, 'long'):
        return None
    for id in ad_group_ids:
        output_status_message("AdGroup successfully added and assigned AdGroupId {0}\n".format(id))
        
def output_targets(targets):
    if not hasattr(targets, 'Target'):
        return None
    for target in targets['Target']:
        output_status_message("Target Id: {0}".format(target.Id))
        output_status_message("Target Name: {0}\n".format(target.Name))

        if hasattr(target.Age, 'Bids'):
            output_status_message("AgeTarget:")
            for bid in target.Age.Bids['AgeTargetBid']:
                output_status_message("\tBidAdjustment: {0}".format(bid.BidAdjustment))
                output_status_message("\tAge: {0}\n".format(bid.Age))
            
        if hasattr(target.DayTime, 'Bids'):
            output_status_message("DayTimeTarget:")
            for bid in target.DayTime.Bids['DayTimeTargetBid']:
                output_status_message("\tBidAdjustment: {0}".format(bid.BidAdjustment))
                output_status_message("\tDay: {0}".format(bid.Day))
                output_status_message("\tFrom Hour: {0}".format(bid.FromHour))
                output_status_message("\tFrom Minute: {0}".format(bid.FromMinute))
                output_status_message("\tTo Hour: {0}".format(bid.ToHour))
                output_status_message("\tTo Minute: {0}\n".format(bid.ToMinute))
            
        if hasattr(target.DeviceOS, 'Bids'):
            output_status_message("DeviceOSTarget:")
            for bid in target.DeviceOS.Bids['DeviceOSTargetBid']:
                output_status_message("\tBidAdjustment: {0}".format(bid.BidAdjustment))
                output_status_message("\tDeviceName: {0}".format(bid.DeviceName))
                   
        if hasattr(target.Gender, 'Bids'):
            output_status_message("GenderTarget:")
            for bid in target.Gender.Bids['GenderTargetBid']:
                output_status_message("\tBidAdjustment: {0}".format(bid.BidAdjustment))
                output_status_message("\tGender: {0}\n".format(bid.Gender))

        if target.Location is not None:
            output_status_message("LocationTarget:")
            output_status_message("\tIntentOption: {0}\n".format(target.Location.IntentOption))
   
            if hasattr(target.Location.CityTarget, 'Bids'):
                output_status_message("\tCityTarget:")
                for bid in target.Location.CityTarget.Bids['CityTargetBid']:
                    output_status_message("\t\tBidAdjustment: {0}".format(bid.BidAdjustment))
                    output_status_message("\t\tCity: {0}\n".format(bid.City))
                    output_status_message("\t\tIsExcluded: {0}\n".format(bid.IsExcluded))

            if hasattr(target.Location.CountryTarget, 'Bids'):
                output_status_message("\tCountryTarget:")
                for bid in target.Location.CountryTarget.Bids['CountryTargetBid']:
                    output_status_message("\t\tBidAdjustment: {0}".format(bid.BidAdjustment))
                    output_status_message("\t\tCountryAndRegion: {0}".format(bid.CountryAndRegion))
                    output_status_message("\t\tIsExcluded: {0}\n".format(bid.IsExcluded))
        
            if hasattr(target.Location.MetroAreaTarget, 'Bids'):
                output_status_message("\tMetroAreaTarget:")
                for bid in target.Location.MetroAreaTarget.Bids['MetroAreaTargetBid']:
                    output_status_message("\t\tBidAdjustment: {0}".format(bid.BidAdjustment))
                    output_status_message("\t\tMetroArea: {0}".format(bid.MetroArea))
                    output_status_message("\t\tIsExcluded: {0}\n".format(bid.IsExcluded))

            if hasattr(target.Location.PostalCodeTarget, 'Bids'):
                output_status_message("\tPostalCodeTarget:")
                for bid in target.Location.PostalCodeTarget.Bids['PostalCodeTargetBid']:
                    output_status_message("\t\tBidAdjustment: {0}".format(bid.BidAdjustment))
                    output_status_message("\t\tPostalCode: {0}".format(bid.PostalCode))
                    output_status_message("\t\tIsExcluded: {0}\n".format(bid.IsExcluded))
            
            if hasattr(target.Location.RadiusTarget, 'Bids'):
                output_status_message("\tRadiusTarget:")
                for bid in target.Location.RadiusTarget.Bids['RadiusTargetBid']:
                    output_status_message("\t\tBidAdjustment: {0}".format(bid.BidAdjustment))
                    output_status_message("\t\tLatitudeDegrees: {0}".format(bid.LatitudeDegrees))
                    output_status_message("\t\tLongitudeDegrees: {0}".format(bid.LongitudeDegrees))
                    output_status_message("\t\tRadius: {0} {1}\n".format(bid.Radius, bid.RadiusUnit))
          
            if hasattr(target.Location.StateTarget, 'Bids'):
                output_status_message("\tStateTarget:")
                for bid in target.Location.StateTarget.Bids['StateTargetBid']:
                    output_status_message("\t\tBidAdjustment: {0}".format(bid.BidAdjustment))
                    output_status_message("\t\tState: {0}".format(bid.State))
                    output_status_message("\t\tIsExcluded: {0}\n".format(bid.IsExcluded))

def output_targets_info(targets_info):
    if not hasattr(targets_info, 'TargetInfo'):
        return None
    for info in targets_info['TargetInfo']:
        output_status_message("Target Id: {0}".format(info.Id))
        output_status_message("Target Name: {0}".format(info.Name))

# Main execution
if __name__ == '__main__':

    try:
        # You should authenticate for Bing Ads production services with a Microsoft Account, 
        # instead of providing the Bing Ads username and password set. 
        # Authentication with a Microsoft Account is currently not supported in Sandbox.
        #authenticate_with_oauth()

        # Uncomment to run with Bing Ads legacy UserName and Password credentials.
        # For example you would use this method to authenticate in sandbox.
        authenticate_with_username()
        
        # Set to an empty user identifier to get the current authenticated Bing Ads user,
        # and then search for all accounts the user may access.
        user=customer_service.GetUser(None).User
        accounts=search_accounts_by_user_id(user.Id)

        # For this example we'll use the first account.
        authorization_data.account_id=accounts['Account'][0].Id
        authorization_data.customer_id=accounts['Account'][0].ParentCustomerId

        # Add a campaign that will later be associated with targets. 

        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.Name="Summer Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description="Summer shoes line."
        campaign.BudgetType='DailyBudgetStandard'
        campaign.MonthlyBudget=50
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.DaylightSaving='true' # Accepts 'true', 'false', True, or False
        campaign.Status='Paused'
        campaigns.Campaign.append(campaign)

        add_campaigns_response=campaign_service.AddCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=campaigns
        )
        campaign_ids={
            'long': add_campaigns_response.CampaignIds['long'] if add_campaigns_response.CampaignIds['long'] else None
        }
        
        output_campaign_ids(campaign_ids)

        # Add an ad group that will later be associated with a target. 

        ad_groups=campaign_service.factory.create('ArrayOfAdGroup')
        ad_group=set_elements_to_none(campaign_service.factory.create('AdGroup'))
        ad_group.Name="Women's Red Shoes"
        ad_group.AdDistribution='Search'
        ad_group.BiddingModel='Keyword'
        ad_group.PricingModel='Cpc'
        ad_group.Network='OwnedAndOperatedAndSyndicatedSearch'
        ad_group.Status='Paused'
        end_date=campaign_service.factory.create('Date')
        end_date.Day=31
        end_date.Month=12
        end_date.Year=strftime("%Y", gmtime())
        ad_group.EndDate=end_date
        search_bid=campaign_service.factory.create('Bid')
        search_bid.Amount=0.09
        ad_group.SearchBid=search_bid
        ad_group.Language='English'
        ad_groups.AdGroup.append(ad_group)

        add_ad_groups_response=campaign_service.AddAdGroups(
            CampaignId=campaign_ids['long'][0],
            AdGroups=ad_groups
        )
        ad_group_ids={
            'long': add_ad_groups_response.AdGroupIds['long'] if add_ad_groups_response.AdGroupIds['long'] else None
        }

        output_ad_group_ids(ad_group_ids)


        # Create targets to associate with the campaign and ad group. 

        campaign_targets=campaign_service.factory.create('ArrayOfTarget')
        campaign_target=set_elements_to_none(campaign_service.factory.create('Target'))
        campaign_target.Name = "My Campaign Target"
        
        campaign_day_time_target=campaign_service.factory.create('DayTimeTarget')
        campaign_day_time_target_bids=campaign_service.factory.create('ArrayOfDayTimeTargetBid')
        campaign_day_time_target_bid=campaign_service.factory.create('DayTimeTargetBid')
        campaign_day_time_target_bid.BidAdjustment=10
        campaign_day_time_target_bid.Day='Monday'
        campaign_day_time_target_bid.FromHour=1
        campaign_day_time_target_bid.FromMinute='Zero'
        campaign_day_time_target_bid.ToHour=12
        campaign_day_time_target_bid.ToMinute='FortyFive'
        campaign_day_time_target_bids.DayTimeTargetBid.append(campaign_day_time_target_bid)
        campaign_day_time_target.Bids=campaign_day_time_target_bids

        campaign_device_os_target=campaign_service.factory.create('DeviceOSTarget')
        campaign_device_os_target_bids=campaign_service.factory.create('ArrayOfDeviceOSTargetBid')
        campaign_device_os_target_bid=campaign_service.factory.create('DeviceOSTargetBid')
        campaign_device_os_target_bid.BidAdjustment = 10
        campaign_device_os_target_bid.DeviceName='Tablets'
        campaign_device_os_target_bids.DeviceOSTargetBid.append(campaign_device_os_target_bid)
        campaign_device_os_target.Bids=campaign_device_os_target_bids

        campaign_location_target=campaign_service.factory.create('LocationTarget')
        campaign_location_target.IntentOption='PeopleIn'

        campaign_metro_area_target=campaign_service.factory.create('MetroAreaTarget')
        campaign_metro_area_target_bids=campaign_service.factory.create('ArrayOfMetroAreaTargetBid')
        campaign_metro_area_target_bid=campaign_service.factory.create('MetroAreaTargetBid')
        campaign_metro_area_target_bid.BidAdjustment = 15
        campaign_metro_area_target_bid.MetroArea="Seattle-Tacoma, WA, WA US"
        campaign_metro_area_target_bid.IsExcluded=False
        campaign_metro_area_target_bids.MetroAreaTargetBid.append(campaign_metro_area_target_bid)
        campaign_metro_area_target.Bids=campaign_metro_area_target_bids
        campaign_location_target.MetroAreaTarget=campaign_metro_area_target

        campaign_radius_target=campaign_service.factory.create('RadiusTarget')
        campaign_radius_target_bids=campaign_service.factory.create('ArrayOfRadiusTargetBid')
        campaign_radius_target_bid=campaign_service.factory.create('RadiusTargetBid')
        campaign_radius_target_bid.BidAdjustment = 50
        campaign_radius_target_bid.LatitudeDegrees = 47.755367
        campaign_radius_target_bid.LongitudeDegrees = -122.091827
        campaign_radius_target_bid.Radius = 5
        campaign_radius_target_bid.RadiusUnit='Kilometers'
        campaign_radius_target_bid.IsExcluded=False
        campaign_radius_target_bids.RadiusTargetBid.append(campaign_radius_target_bid)
        campaign_radius_target.Bids=campaign_radius_target_bids
        campaign_location_target.RadiusTarget=campaign_radius_target

        campaign_target.DayTime=campaign_day_time_target
        campaign_target.DeviceOS=campaign_device_os_target
        campaign_target.Location=campaign_location_target
        campaign_targets.Target.append(campaign_target)
        
        ad_group_targets=campaign_service.factory.create('ArrayOfTarget')
        ad_group_target=set_elements_to_none(campaign_service.factory.create('Target'))
        ad_group_target.Name = "My Ad Group Target"

        ad_group_day_time_target=campaign_service.factory.create('DayTimeTarget')
        ad_group_day_time_target_bids=campaign_service.factory.create('ArrayOfDayTimeTargetBid')
        ad_group_day_time_target_bid=campaign_service.factory.create('DayTimeTargetBid')
        ad_group_day_time_target_bid.BidAdjustment=10
        ad_group_day_time_target_bid.Day='Friday'
        ad_group_day_time_target_bid.FromHour=1
        ad_group_day_time_target_bid.FromMinute='Zero'
        ad_group_day_time_target_bid.ToHour=12
        ad_group_day_time_target_bid.ToMinute='FortyFive'
        ad_group_day_time_target_bids.DayTimeTargetBid.append(ad_group_day_time_target_bid)
        ad_group_day_time_target.Bids=ad_group_day_time_target_bids

        ad_group_target.DayTime=ad_group_day_time_target
        ad_group_targets.Target.append(ad_group_target)

        # Each customer has a target library that can be used to set up targeting for any campaign
        # or ad group within the specified customer. 

        # Add a target to the library and associate it with the campaign.
        campaign_target_id=campaign_service.AddTargetsToLibrary(Targets=campaign_targets)['long'][0]
        output_status_message("Added Target Id: {0}\n".format(campaign_target_id))
        campaign_service.SetTargetToCampaign(
            CampaignId=campaign_ids['long'][0], 
            TargetId=campaign_target_id
        )
        output_status_message("Associated CampaignId {0} with TargetId {1}.\n".format(campaign_ids['long'][0], campaign_target_id))

        # Add a target to the library and associate it with the ad group.
        ad_group_target_id=campaign_service.AddTargetsToLibrary(Targets=ad_group_targets)['long'][0]
        output_status_message("Added Target Id: {0}\n".format(ad_group_target_id))
        campaign_service.SetTargetToAdGroup(ad_group_ids['long'][0], ad_group_target_id)
        output_status_message("Associated AdGroupId {0} with TargetId {1}.\n".format(ad_group_ids['long'][0], ad_group_target_id))

        # Get and print the targets with the GetTargetsByIds operation
        output_status_message("Get Campaign and AdGroup targets: \n")
        targets=campaign_service.GetTargetsByIds(
            TargetIds={'long': [campaign_target_id, ad_group_target_id] }
        )
        output_targets(targets)

        # Update the ad group's target as a Target object with additional target types.
        # Existing target types such as DayTime must be specified 
        # or they will not be included in the updated target.

        targets=campaign_service.factory.create('ArrayOfTarget')
        target=set_elements_to_none(campaign_service.factory.create('Target'))
        
        age_target=campaign_service.factory.create('AgeTarget')
        age_target_bids=campaign_service.factory.create('ArrayOfAgeTargetBid')
        age_target_bid=campaign_service.factory.create('AgeTargetBid')
        age_target_bid.BidAdjustment = 10
        age_target_bid.Age='EighteenToTwentyFive'
        age_target_bids.AgeTargetBid.append(age_target_bid)
        age_target.Bids=age_target_bids

        day_time_target=campaign_service.factory.create('DayTimeTarget')
        day_time_target_bids=campaign_service.factory.create('ArrayOfDayTimeTargetBid')
        day_time_target_bid=campaign_service.factory.create('DayTimeTargetBid')
        day_time_target_bid.BidAdjustment=10
        day_time_target_bid.Day='Friday'
        day_time_target_bid.FromHour=1
        day_time_target_bid.FromMinute='Zero'
        day_time_target_bid.ToHour=12
        day_time_target_bid.ToMinute='FortyFive'
        day_time_target_bids.DayTimeTargetBid.append(day_time_target_bid)
        day_time_target.Bids=day_time_target_bids

        device_os_target=campaign_service.factory.create('DeviceOSTarget')
        device_os_target_bids=campaign_service.factory.create('ArrayOfDeviceOSTargetBid')
        device_os_target_bid=campaign_service.factory.create('DeviceOSTargetBid')
        device_os_target_bid.BidAdjustment = 20
        device_os_target_bid.DeviceName='Tablets'
        device_os_target_bids.DeviceOSTargetBid.append(device_os_target_bid)
        device_os_target.Bids=device_os_target_bids

        gender_target=campaign_service.factory.create('GenderTarget')
        gender_target_bids=campaign_service.factory.create('ArrayOfGenderTargetBid')
        gender_target_bid=campaign_service.factory.create('GenderTargetBid')
        gender_target_bid.BidAdjustment = 10
        gender_target_bid.Gender='Female'
        gender_target_bids.GenderTargetBid.append(gender_target_bid)
        gender_target.Bids=gender_target_bids

        country_target=campaign_service.factory.create('CountryTarget')
        country_target_bids=campaign_service.factory.create('ArrayOfCountryTargetBid')
        country_target_bid=campaign_service.factory.create('CountryTargetBid')
        country_target_bid.BidAdjustment=10
        country_target_bid.CountryAndRegion="US"
        country_target_bid.IsExcluded=False
        country_target_bids.CountryTargetBid.append(country_target_bid)
        country_target.Bids=country_target_bids
    
        metro_area_target=campaign_service.factory.create('MetroAreaTarget')
        metro_area_target_bids=campaign_service.factory.create('ArrayOfMetroAreaTargetBid')
        metro_area_target_bid=campaign_service.factory.create('MetroAreaTargetBid')
        metro_area_target_bid.BidAdjustment=15
        metro_area_target_bid.MetroArea="Seattle-Tacoma, WA, WA US"
        metro_area_target_bid.IsExcluded=False
        metro_area_target_bids.MetroAreaTargetBid.append(metro_area_target_bid)
        metro_area_target.Bids=metro_area_target_bids

        postal_code_target=campaign_service.factory.create('PostalCodeTarget')
        postal_code_target_bids=campaign_service.factory.create('ArrayOfPostalCodeTargetBid')
        postal_code_target_bid=campaign_service.factory.create('PostalCodeTargetBid')
        # Bid adjustments are not allowed for location exclusions. 
        # If IsExcluded is true, this element will be ignored.
        postal_code_target_bid.BidAdjustment=10
        postal_code_target_bid.PostalCode="98052, WA US"
        postal_code_target_bid.IsExcluded=True
        postal_code_target_bids.PostalCodeTargetBid.append(postal_code_target_bid)
        postal_code_target.Bids=postal_code_target_bids

        radius_target=campaign_service.factory.create('RadiusTarget')
        radius_target_bids=campaign_service.factory.create('ArrayOfRadiusTargetBid')
        radius_target_bid=campaign_service.factory.create('RadiusTargetBid')
        radius_target_bid.BidAdjustment=10
        radius_target_bid.LatitudeDegrees=47.755367
        radius_target_bid.LongitudeDegrees=-122.091827
        radius_target_bid.Radius=11
        radius_target_bid.RadiusUnit='Miles'
        radius_target_bid.IsExcluded=False
        radius_target_bids.RadiusTargetBid.append(radius_target_bid)
        radius_target.Bids=radius_target_bids

        location_target=campaign_service.factory.create('LocationTarget')
        location_target.IntentOption='PeopleSearchingForOrViewingPages'
        location_target.CountryTarget=country_target
        location_target.MetroAreaTarget=metro_area_target
        location_target.PostalCodeTarget=postal_code_target
        location_target.RadiusTarget=radius_target
        
        target.Age=age_target
        target.DayTime=day_time_target
        target.DeviceOS=device_os_target
        target.Gender=gender_target
        target.Id = ad_group_target_id
        target.Location=location_target
        target.Name = "My Target"
        targets.Target.append(target)

        # Update the Target object associated with the ad group. 
        campaign_service.UpdateTargetsInLibrary(Targets=targets)
        output_status_message("Updated the ad group level target as a Target object.\n")

        # Get and print the targets with the GetTargetsByIds operation
        output_status_message("Get Campaign and AdGroup targets: \n")
        targets=campaign_service.GetTargetsByIds(
            TargetIds={'long': [campaign_target_id, ad_group_target_id] }
        )
        output_targets(targets)

        # Get all new and existing targets in the customer library, whether or not they are
        # associated with campaigns or ad groups.

        all_targets_info=campaign_service.GetTargetsInfoFromLibrary()
        output_status_message("All target identifiers and names from the customer library: \n")
        output_targets_info(all_targets_info)

        # Delete the campaign, ad group, and targets that were previously added. 
        # DeleteCampaigns would remove the campaign and ad group, as well as the association
        # between ad groups and campaigns. To explicitly delete the association between an entity 
        # and the target, use DeleteTargetFromCampaign and DeleteTargetFromAdGroup respectively.

        campaign_service.DeleteTargetFromCampaign(CampaignId=campaign_ids['long'][0])
        campaign_service.DeleteTargetFromAdGroup(AdGroupId=ad_group_ids['long'][0])

        campaign_service.DeleteCampaigns(
            AccountId=authorization_data.account_id,
            CampaignIds=campaign_ids
        )

        for campaign_id in campaign_ids['long']:
            output_status_message("Deleted CampaignId {0}\n".format(campaign_id))

        # DeleteCampaigns deletes the association between the campaign and target, but does not 
        # delete the target from the customer library. 
        # Call the DeleteTargetsFromLibrary operation for each target that you want to delete. 
        # You must specify an array with exactly one item.

        campaign_service.DeleteTargetsFromLibrary(TargetIds={'long': [campaign_target_id] })
        output_status_message("Deleted TargetId {0}\n".format(campaign_target_id))

        campaign_service.DeleteTargetsFromLibrary(TargetIds={'long': [ad_group_target_id] })
        output_status_message("Deleted TargetId {0}\n".format(ad_group_target_id))
        
        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

