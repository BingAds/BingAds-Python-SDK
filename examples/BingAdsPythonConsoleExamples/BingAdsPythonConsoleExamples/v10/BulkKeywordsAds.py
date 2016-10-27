from bingads.service_client import ServiceClient
from bingads.authorization import *
from bingads.v10 import *
from bingads.v10.bulk import *

import sys
import webbrowser
from time import gmtime, strftime
from suds import WebFault
from decimal import Decimal

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

    BUDGET_ID_KEY=-20
    CAMPAIGN_ID_KEY=-123
    AD_GROUP_ID_KEY=-1234

    # The directory for the bulk files.
    FILE_DIRECTORY='c:/bulk/'

    # The name of the bulk download file.
    DOWNLOAD_FILE_NAME='download.csv'

    #The name of the bulk upload file.
    UPLOAD_FILE_NAME='upload.csv'

    # The name of the bulk upload result file.
    RESULT_FILE_NAME='result.csv'

    # The bulk file extension type.
    FILE_FORMAT = DownloadFileType.csv

    # The bulk file extension type as a string.
    FILE_TYPE = 'Csv'

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

def print_percent_complete(progress):
    output_status_message("Percent Complete: {0}\n".format(progress.percent_complete))

def output_status_message(message):
    print(message)

def output_bulk_performance_data(performance_data):
    if performance_data is not None:
        output_status_message("AverageCostPerClick: {0}".format(performance_data.average_cost_per_click))
        output_status_message("AverageCostPerThousandImpressions: {0}".format(performance_data.average_cost_per_thousand_impressions))
        output_status_message("AveragePosition: {0}".format(performance_data.average_position))
        output_status_message("Clicks: {0}".format(performance_data.clicks))
        output_status_message("ClickThroughRate: {0}".format(performance_data.click_through_rate))
        output_status_message("Conversions: {0}".format(performance_data.conversions))
        output_status_message("CostPerConversion: {0}".format(performance_data.cost_per_conversion))
        output_status_message("Impressions: {0}".format(performance_data.impressions))
        output_status_message("Spend: {0}".format(performance_data.spend))

def output_bulk_quality_score_data(quality_score_data):
    if quality_score_data is not None:
        output_status_message("KeywordRelevance: {0}".format(quality_score_data.keyword_relevance))
        output_status_message("LandingPageRelevance: {0}".format(quality_score_data.landing_page_relevance))
        output_status_message("LandingPageUserExperience: {0}".format(quality_score_data._landing_page_user_experience))
        output_status_message("QualityScore: {0}".format(quality_score_data.quality_score))

def output_bulk_bid_suggestions(bid_suggestions):
    if bid_suggestions is not None:
        output_status_message("BestPosition: {0}".format(bid_suggestions.best_position))
        output_status_message("MainLine: {0}".format(bid_suggestions.main_line))
        output_status_message("FirstPage: {0}".format(bid_suggestions.first_page))

def output_bulk_budgets(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkBudget: \n")
        output_status_message("AccountId: {0}".format(entity.account_id))
        output_status_message("ClientId: {0}".format(entity.client_id))

        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))
            
        output_status_message("Status: {0}".format(entity.status))

        # Output the Campaign Management Budget Object
        output_budget(entity.budget)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_budget(budget):
    if budget is not None:
        output_status_message("Amount: {0}".format(budget.Amount))
        output_status_message("AssociationCount: {0}".format(budget.AssociationCount))
        output_status_message("BudgetType: {0}".format(budget.BudgetType))
        output_status_message("Id: {0}".format(budget.Id))
        output_status_message("Name: {0}\n".format(budget.Name))

def output_bulk_campaigns(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaign: \n")
        output_status_message("AccountId: {0}".format(entity.account_id))
        output_status_message("ClientId: {0}".format(entity.client_id))

        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        output_bulk_performance_data(entity.performance_data)
        output_bulk_quality_score_data(entity.quality_score_data)

        # Output the Campaign Management Campaign Object
        output_campaign(entity.campaign)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_campaign(campaign):
    if campaign is not None:
        if hasattr(campaign, 'BiddingScheme'): 
            output_bidding_scheme(campaign.BiddingScheme)
        if hasattr(campaign, 'BudgetId'): 
            output_status_message("BudgetId: {0}".format(campaign.BudgetId))
        output_status_message("BudgetType: {0}".format(campaign.BudgetType))
        if campaign.CampaignType is not None:
            for campaign_type in campaign.CampaignType:
                output_status_message("CampaignType: {0}".format(campaign_type))
        else:
            output_status_message("CampaignType: None")
        output_status_message("DailyBudget: {0}".format(campaign.DailyBudget))
        output_status_message("Description: {0}".format(campaign.Description))
        output_status_message("ForwardCompatibilityMap: ")
        if campaign.ForwardCompatibilityMap is not None and len(campaign.ForwardCompatibilityMap.KeyValuePairOfstringstring) > 0:
            for pair in campaign.ForwardCompatibilityMap['KeyValuePairOfstringstring']:
                output_status_message("Key: {0}".format(pair.key))
                output_status_message("Value: {0}".format(pair.value))
        output_status_message("Id: {0}".format(campaign.Id))
        output_status_message("MonthlyBudget: {0}".format(campaign.MonthlyBudget))
        output_status_message("Name: {0}".format(campaign.Name))
        output_status_message("NativeBidAdjustment: {0}".format(campaign.NativeBidAdjustment))
        output_status_message("Settings: ")
        for setting in campaign.Settings.Setting:
            if setting.Type == 'ShoppingSetting':
                output_status_message("\tShoppingSetting: ")
                output_status_message("\t\tPriority: {0}".format(setting.Priority))
                output_status_message("\t\tSalesCountryCode: {0}".format(setting.SalesCountryCode))
                output_status_message("\t\tStoreId: {0}".format(setting.StoreId))
        output_status_message("Status: {0}".format(campaign.Status))
        output_status_message("TimeZone: {0}".format(campaign.TimeZone))
        output_status_message("TrackingUrlTemplate: {0}".format(campaign.TrackingUrlTemplate))
        output_status_message("UrlCustomParameters: ")
        if campaign.UrlCustomParameters is not None and campaign.UrlCustomParameters.Parameters is not None:
            for custom_parameter in campaign.UrlCustomParameters.Parameters['CustomParameter']:
                output_status_message("\tKey: {0}".format(custom_parameter.Key))
                output_status_message("\tValue: {0}".format(custom_parameter.Value))

def output_bulk_ad_groups(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkAdGroup: \n")
        output_status_message("Campaign Id: {0}".format(entity.campaign_id))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        output_status_message("IsExpired: {0}".format(entity.is_expired))
        
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        output_bulk_performance_data(entity.performance_data)
        output_bulk_quality_score_data(entity.quality_score_data)

        # Output the Campaign Management AdGroup Object
        output_ad_group(entity.ad_group)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_ad_group(ad_group):
    if ad_group is not None:
        output_status_message("AdDistribution: {0}".format(ad_group.AdDistribution))
        output_status_message("AdRotation: {0}".format(
            ad_group.AdRotation.Type if ad_group.AdRotation is not None else None)
        )
        output_status_message("BiddingModel: {0}".format(ad_group.BiddingModel))
        output_bidding_scheme(ad_group.BiddingScheme)
        output_status_message("ForwardCompatibilityMap: ")
        if ad_group.ForwardCompatibilityMap is not None and len(ad_group.ForwardCompatibilityMap.KeyValuePairOfstringstring) > 0:
            for pair in ad_group.ForwardCompatibilityMap['KeyValuePairOfstringstring']:
                output_status_message("Key: {0}".format(pair.key))
                output_status_message("Value: {0}".format(pair.value))
        output_status_message("Id: {0}".format(ad_group.Id))
        output_status_message("Language: {0}".format(ad_group.Language))
        output_status_message("Name: {0}".format(ad_group.Name))
        output_status_message("NativeBidAdjustment: {0}".format(ad_group.NativeBidAdjustment))
        output_status_message("Network: {0}".format(ad_group.Network))
        output_status_message("PricingModel: {0}".format(ad_group.PricingModel))
        output_status_message("RemarketingTargetingSetting: {0}".format(ad_group.RemarketingTargetingSetting))
        output_status_message("SearchBid: {0}".format(
            ad_group.SearchBid.Amount if ad_group.SearchBid is not None else None)
        )
        output_status_message("Status: {0}".format(ad_group.Status))
        output_status_message("TrackingUrlTemplate: {0}".format(ad_group.TrackingUrlTemplate))
        output_status_message("UrlCustomParameters: ")
        if ad_group.UrlCustomParameters is not None and ad_group.UrlCustomParameters.Parameters is not None:
            for custom_parameter in ad_group.UrlCustomParameters.Parameters['CustomParameter']:
                output_status_message("\tKey: {0}".format(custom_parameter.Key))
                output_status_message("\tValue: {0}".format(custom_parameter.Value))

def output_bulk_expanded_text_ads(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkExpandedTextAd: \n")
        output_status_message("AdGroup Id: {0}".format(entity.ad_group_id))
        output_status_message("AdGroup Name: {0}".format(entity.ad_group_name))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        output_bulk_performance_data(entity.performance_data)

        # Output the Campaign Management ExpandedTextAd Object
        output_expanded_text_ad(entity.expanded_text_ad)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_ad(ad):
    if ad is not None:
        output_status_message("DevicePreference: {0}".format(ad.DevicePreference))
        output_status_message("EditorialStatus: {0}".format(ad.EditorialStatus))
        output_status_message("FinalMobileUrls: ")
        if ad.FinalMobileUrls is not None:
            for final_mobile_url in ad.FinalMobileUrls['string']:
                output_status_message("\t{0}".format(final_mobile_url))
        output_status_message("FinalUrls: ")
        if ad.FinalUrls is not None:
            for final_url in ad.FinalUrls['string']:
                output_status_message("\t{0}".format(final_url))
        output_status_message("ForwardCompatibilityMap: ")
        if ad.ForwardCompatibilityMap is not None and len(ad.ForwardCompatibilityMap.KeyValuePairOfstringstring) > 0:
            for pair in ad.ForwardCompatibilityMap['KeyValuePairOfstringstring']:
                output_status_message("Key: {0}".format(pair.key))
                output_status_message("Value: {0}".format(pair.value))
        output_status_message("Id: {0}".format(ad.Id))
        output_status_message("Status: {0}".format(ad.Status))
        output_status_message("TrackingUrlTemplate: {0}".format(ad.TrackingUrlTemplate))
        output_status_message("UrlCustomParameters: ")
        if ad.UrlCustomParameters is not None and ad.UrlCustomParameters.Parameters is not None:
            for custom_parameter in ad.UrlCustomParameters.Parameters['CustomParameter']:
                output_status_message("\tKey: {0}".format(custom_parameter.Key))
                output_status_message("\tValue: {0}".format(custom_parameter.Value))

def output_expanded_text_ad(ad):
    if ad is not None:
        # Output inherited properties of the Ad base class.
        output_ad(ad)
            
        # Output properties that are specific to the ExpandedTextAd
        output_status_message("DisplayUrl: {0}".format(ad.DisplayUrl))
        output_status_message("Path1: {0}".format(ad.Path1))
        output_status_message("Path2: {0}".format(ad.Path2))
        output_status_message("Text: {0}".format(ad.Text))
        output_status_message("TitlePart1: {0}".format(ad.TitlePart1))
        output_status_message("TitlePart2: {0}".format(ad.TitlePart2))
        
def output_bulk_keywords(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkKeyword: \n")
        output_status_message("AdGroup Id: {0}".format(entity.ad_group_id))
        output_status_message("AdGroup Name: {0}".format(entity.ad_group_name))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        output_bulk_performance_data(entity.performance_data)
        output_bulk_quality_score_data(entity.quality_score_data)
        output_bulk_bid_suggestions(entity.bid_suggestions)

        # Output the Campaign Management Keyword Object
        output_keyword(entity.keyword)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_keyword(keyword):
    if keyword is not None:
        output_status_message("Bid.Amount: {0}".format(
            keyword.Bid.Amount if keyword.Bid is not None else None)
        )
        output_bidding_scheme(keyword.BiddingScheme)
        output_status_message("DestinationUrl: {0}".format(keyword.DestinationUrl))
        output_status_message("EditorialStatus: {0}".format(keyword.EditorialStatus))
        output_status_message("FinalMobileUrls: ")
        if keyword.FinalMobileUrls is not None:
            for final_mobile_url in keyword.FinalMobileUrls['string']:
                output_status_message("\t{0}".format(final_mobile_url))
        output_status_message("FinalUrls: ")
        if keyword.FinalUrls is not None:
            for final_url in keyword.FinalUrls['string']:
                output_status_message("\t{0}".format(final_url))
        output_status_message("ForwardCompatibilityMap: ")
        if keyword.ForwardCompatibilityMap is not None and len(keyword.ForwardCompatibilityMap.KeyValuePairOfstringstring) > 0:
            for pair in keyword.ForwardCompatibilityMap['KeyValuePairOfstringstring']:
                output_status_message("Key: {0}".format(pair.key))
                output_status_message("Value: {0}".format(pair.value))
        output_status_message("Id: {0}".format(keyword.Id))
        output_status_message("MatchType: {0}".format(keyword.MatchType))
        output_status_message("Param1: {0}".format(keyword.Param1))
        output_status_message("Param2: {0}".format(keyword.Param2))
        output_status_message("Param3: {0}".format(keyword.Param3))
        output_status_message("Status: {0}".format(keyword.Status))
        output_status_message("Text: {0}".format(keyword.Text))
        output_status_message("TrackingUrlTemplate: {0}".format(keyword.TrackingUrlTemplate))
        output_status_message("UrlCustomParameters: ")
        if keyword.UrlCustomParameters is not None and keyword.UrlCustomParameters.Parameters is not None:
            for custom_parameter in keyword.UrlCustomParameters.Parameters['CustomParameter']:
                output_status_message("\tKey: {0}".format(custom_parameter.Key))
                output_status_message("\tValue: {0}".format(custom_parameter.Value))

def output_bidding_scheme(bidding_scheme):
    if bidding_scheme is None or type(bidding_scheme) == type(campaign_service.factory.create('ns0:BiddingScheme')):
        return
    elif type(bidding_scheme) == type(campaign_service.factory.create('ns0:EnhancedCpcBiddingScheme')):
        output_status_message("BiddingScheme: EnhancedCpc")
    elif type(bidding_scheme) == type(campaign_service.factory.create('ns0:InheritFromParentBiddingScheme')):
        output_status_message("BiddingScheme: InheritFromParent")
    elif type(bidding_scheme) == type(campaign_service.factory.create('ns0:MaxConversionsBiddingScheme')):
        output_status_message("BiddingScheme: MaxConversions")
    elif type(bidding_scheme) == type(campaign_service.factory.create('ns0:ManualCpcBiddingScheme')):
        output_status_message("BiddingScheme: ManualCpc")
    elif type(bidding_scheme) == type(campaign_service.factory.create('ns0:TargetCpaBiddingScheme')):
        output_status_message("BiddingScheme: TargetCpa")
    elif type(bidding_scheme) == type(campaign_service.factory.create('ns0:MaxClicksBiddingScheme')):
        output_status_message("BiddingScheme: MaxClicks")

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

def write_entities_and_upload_file(upload_entities):
    # Writes the specified entities to a local file and uploads the file. We could have uploaded directly
    # without writing to file. This example writes to file as an exercise so that you can view the structure 
    # of the bulk records being uploaded as needed. 
    writer=BulkFileWriter(FILE_DIRECTORY+UPLOAD_FILE_NAME);
    for entity in upload_entities:
        writer.write_entity(entity)
    writer.close()

    file_upload_parameters=FileUploadParameters(
        result_file_directory=FILE_DIRECTORY,
        compress_upload_file=True,
        result_file_name=RESULT_FILE_NAME,
        overwrite_result_file=True,
        upload_file_path=FILE_DIRECTORY+UPLOAD_FILE_NAME,
        response_mode='ErrorsAndResults'
    )

    bulk_file_path=bulk_service.upload_file(file_upload_parameters, progress=print_percent_complete)

    download_entities=[]
    entities_generator=read_entities_from_bulk_file(file_path=bulk_file_path, result_file_type=ResultFileType.upload, file_format=FILE_FORMAT)
    for entity in entities_generator:
        download_entities.append(entity)

    return download_entities

def download_file(download_parameters):
    bulk_file_path=bulk_service.download_file(download_parameters, progress=print_percent_complete)

    download_entities=[]
    entities_generator=read_entities_from_bulk_file(file_path=bulk_file_path, result_file_type=ResultFileType.full_download, file_format=FILE_FORMAT)
    for entity in entities_generator:
        download_entities.append(entity)

    return download_entities

def read_entities_from_bulk_file(file_path, result_file_type, file_format):
    with BulkFileReader(file_path=file_path, result_file_type=result_file_type, file_format=file_format) as reader:
        for entity in reader:
            yield entity

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
        user_id=None
        user=customer_service.GetUser(None).User
        accounts=search_accounts_by_user_id(user.Id)
        
        # For this example we'll use the first account.
        authorization_data.account_id=accounts['Account'][0].Id
        authorization_data.customer_id=accounts['Account'][0].ParentCustomerId

        # Determine whether you are able to add shared budgets by checking the pilot flags.

        enabled_for_shared_budgets = False
        feature_pilot_flags = customer_service.GetCustomerPilotFeatures(authorization_data.customer_id)

        # The pilot flag value for shared budgets is 263.
        # Pilot flags apply to all accounts within a given customer.
        if(263 in feature_pilot_flags['int']):
            enabled_for_shared_budgets = True
        
        # If the customer is enabled for shared budgets, let's create a new budget and
        # share it with a new campaign.

        upload_entities=[]
        
        if enabled_for_shared_budgets:
            bulk_budget=BulkBudget()
            bulk_budget.client_id='YourClientIdGoesHere'
            budget=set_elements_to_none(campaign_service.factory.create('Budget'))
            budget.Amount=50
            budget.BudgetType='DailyBudgetStandard'
            budget.Id=BUDGET_ID_KEY
            budget.Name="My Shared Budget " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
            bulk_budget.budget=budget
            upload_entities.append(bulk_budget)

        
        bulk_campaign=BulkCampaign()
        
        # The client_id may be used to associate records in the bulk upload file with records in the results file. The value of this field  
        # is not used or stored by the server; it is simply copied from the uploaded record to the corresponding result record. 
        # Note: This bulk file Client Id is not related to an application Client Id for OAuth. 
        
        bulk_campaign.client_id='YourClientIdGoesHere'
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        
        # When using the Campaign Management service, the Id cannot be set. In the context of a BulkCampaign, the Id is optional  
        # and may be used as a negative reference key during bulk upload. For example the same negative reference key for the campaign Id  
        # will be used when adding new ad groups to this new campaign, or when associating ad extensions with the campaign. 

        campaign.Id=CAMPAIGN_ID_KEY
        campaign.Name="Summer Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description="Summer shoes line."

        # You must choose to set either the shared  budget ID or daily amount.
        # You can set one or the other, but you may not set both.
        campaign.BudgetId=BUDGET_ID_KEY if enabled_for_shared_budgets else 0
        campaign.DailyBudget=0 if enabled_for_shared_budgets else 50
        campaign.BudgetType='DailyBudgetStandard'
        
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.Status='Paused'

        # DaylightSaving is not supported in the Bulk file schema. Whether or not you specify it in a BulkCampaign,
        # the value is not written to the Bulk file, and by default DaylightSaving is set to true.
        campaign.DaylightSaving='True'

        # You can set your campaign bid strategy to Enhanced CPC (EnhancedCpcBiddingScheme) 
        # and then, at any time, set an individual ad group or keyword bid strategy to 
        # Manual CPC (ManualCpcBiddingScheme).
        # For campaigns you can use either of the EnhancedCpcBiddingScheme or ManualCpcBiddingScheme objects. 
        # If you do not set this element, then ManualCpcBiddingScheme is used by default.
        campaign_bidding_scheme=set_elements_to_none(campaign_service.factory.create('ns0:EnhancedCpcBiddingScheme'))
        campaign.BiddingScheme=campaign_bidding_scheme
                
        # Used with FinalUrls shown in the expanded text ads that we will add below.
        campaign.TrackingUrlTemplate="http://tracker.example.com/?season={_season}&promocode={_promocode}&u={lpurl}"

        bulk_campaign.campaign=campaign

        bulk_ad_group=BulkAdGroup()
        bulk_ad_group.campaign_id=CAMPAIGN_ID_KEY
        ad_group=set_elements_to_none(campaign_service.factory.create('AdGroup'))
        ad_group.Id=AD_GROUP_ID_KEY
        ad_group.Name="Women's Red Shoes"
        ad_group.AdDistribution='Search'
        ad_group.BiddingModel='Keyword'
        ad_group.PricingModel='Cpc'
        end_date=campaign_service.factory.create('Date')
        end_date.Day=31
        end_date.Month=12
        end_date.Year=strftime("%Y", gmtime())
        ad_group.EndDate=end_date
        search_bid=campaign_service.factory.create('Bid')
        search_bid.Amount=0.09
        ad_group.SearchBid=search_bid
        ad_group.Language='English'

        # For ad groups you can use either of the InheritFromParentBiddingScheme or ManualCpcBiddingScheme objects. 
        # If you do not set this element, then InheritFromParentBiddingScheme is used by default.
        ad_group_bidding_scheme=set_elements_to_none(campaign_service.factory.create('ns0:ManualCpcBiddingScheme'))
        ad_group.BiddingScheme=ad_group_bidding_scheme

        # You could use a tracking template which would override the campaign level
        # tracking template. Tracking templates defined for lower level entities 
        # override those set for higher level entities.
        # In this example we are using the campaign level tracking template.
        ad_group.TrackingUrlTemplate=None

        bulk_ad_group.ad_group=ad_group

        # In this example only the first 3 ads should succeed. 
        # The Title of the fourth ad is empty and not valid,
        # and the fifth ad is a duplicate of the second ad 

        bulk_expanded_text_ads=[]

        for index in range(5):
            bulk_expanded_text_ad=BulkExpandedTextAd()
            bulk_expanded_text_ad.ad_group_id=AD_GROUP_ID_KEY
            expanded_text_ad=set_elements_to_none(campaign_service.factory.create('ExpandedTextAd'))
            expanded_text_ad.TitlePart1='Contoso'
            expanded_text_ad.TitlePart2='Fast & Easy Setup'
            expanded_text_ad.Text='Huge Savings on red shoes.'
            expanded_text_ad.Path1='seattle'
            expanded_text_ad.Path2='shoe sale'
            expanded_text_ad.Type='ExpandedText'
            expanded_text_ad.Status=None
            expanded_text_ad.EditorialStatus=None
            
            # With FinalUrls you can separate the tracking template, custom parameters, and 
            # landing page URLs.
            final_urls=campaign_service.factory.create('ns4:ArrayOfstring')
            final_urls.string.append('http://www.contoso.com/womenshoesale')
            expanded_text_ad.FinalUrls=final_urls

            # Final Mobile URLs can also be used if you want to direct the user to a different page 
            # for mobile devices.
            final_mobile_urls=campaign_service.factory.create('ns4:ArrayOfstring')
            final_mobile_urls.string.append('http://mobile.contoso.com/womenshoesale')
            expanded_text_ad.FinalMobileUrls=final_mobile_urls

            # You could use a tracking template which would override the campaign level
            # tracking template. Tracking templates defined for lower level entities 
            # override those set for higher level entities.
            # In this example we are using the campaign level tracking template.
            expanded_text_ad.TrackingUrlTemplate=None

            # Set custom parameters that are specific to this ad, 
            # and can be used by the ad, ad group, campaign, or account level tracking template. 
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
            expanded_text_ad.UrlCustomParameters=url_custom_parameters
            bulk_expanded_text_ad.ad=expanded_text_ad
            bulk_expanded_text_ads.append(bulk_expanded_text_ad)

        bulk_expanded_text_ads[1].ad.Title="Quick & Easy Setup"
        bulk_expanded_text_ads[2].ad.Title="Fast & Simple Setup"
        bulk_expanded_text_ads[3].ad.Title=''
        bulk_expanded_text_ads[4].ad.Title="Quick & Easy Setup"

        # In this example only the second keyword should succeed. The Text of the first keyword exceeds the limit,
        # and the third keyword is a duplicate of the second keyword.

        bulk_keywords=[]

        for index in range(3):
            bulk_keyword=BulkKeyword()
            bulk_keyword.ad_group_id=AD_GROUP_ID_KEY
            keyword=set_elements_to_none(campaign_service.factory.create('Keyword'))
            keyword.Bid=set_elements_to_none(campaign_service.factory.create('Bid'))
            keyword.Bid.Amount=0.47
            keyword.Param2='10% Off'
            keyword.MatchType='Broad'
            keyword.Text='Brand-A Shoes'

            # For keywords you can use either of the InheritFromParentBiddingScheme or ManualCpcBiddingScheme objects. 
            # If you do not set this element, then InheritFromParentBiddingScheme is used by default.
            keyword_bidding_scheme=set_elements_to_none(campaign_service.factory.create('ns0:InheritFromParentBiddingScheme'))
            keyword.BiddingScheme=keyword_bidding_scheme

            bulk_keyword.keyword=keyword
            bulk_keywords.append(bulk_keyword)

        bulk_keywords[0].keyword.Text=(
            "Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes "
		    "Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes "
		    "Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes"
        )

        # Write the entities created above, to temporary memory. 
        # Dependent entities such as BulkKeyword must be written after any dependencies,   
        # for example the BulkCampaign and BulkAdGroup. 

        upload_entities.append(bulk_campaign)
        upload_entities.append(bulk_ad_group)
        for bulk_expanded_text_ad in bulk_expanded_text_ads:
            upload_entities.append(bulk_expanded_text_ad)
        for bulk_keyword in bulk_keywords:
            upload_entities.append(bulk_keyword)      
        
        output_status_message("\nAdding campaign, budget, ad group, keywords, and ads . . .")
        download_entities=write_entities_and_upload_file(upload_entities)

        budget_results=[]
        campaign_results=[]
        adgroup_results=[]
        keyword_results=[]

        for entity in download_entities:
            if isinstance(entity, BulkBudget):
                budget_results.append(entity)
                output_bulk_budgets([entity])
            if isinstance(entity, BulkCampaign):
                campaign_results.append(entity)
                output_bulk_campaigns([entity])
            if isinstance(entity, BulkAdGroup):
                adgroup_results.append(entity)
                output_bulk_ad_groups([entity])
            if isinstance(entity, BulkExpandedTextAd):
                output_bulk_expanded_text_ads([entity])
            if isinstance(entity, BulkKeyword):
                keyword_results.append(entity)
                output_bulk_keywords([entity])


        # Here is a simple example that updates the keyword bid to use the ad group bid.

        update_bulk_keyword=BulkKeyword()
        update_bulk_keyword.ad_group_id=adgroup_results[0].ad_group.Id
        update_keyword=campaign_service.factory.create('Keyword')

        update_keyword.Id=next((keyword_result.keyword.Id for keyword_result in keyword_results if 
                                keyword_result.keyword.Id is not None and keyword_result.ad_group_id==update_bulk_keyword.ad_group_id), "None")

        # You can set the Bid.Amount property to change the keyword level bid.
        update_keyword.Bid=campaign_service.factory.create('Bid')
        update_keyword.Bid.Amount=0.46

        # The keyword bid will not be updated if the Bid property is not specified or if you create
        # an empty Bid.
        #update_keyword.Bid=campaign_service.factory.create('Bid')
        
        # The keyword level bid will be deleted ("delete_value" will be written in the bulk upload file), and
        # the keyword will effectively inherit the ad group level bid if you explicitly set the Bid property to None. 
        #update_keyword.Bid=None

        # It is important to note that the above behavior differs from the Bid settings that
        # are used to update keywords with the Campaign Management servivce.
        # When using the Campaign Management service with the Bing Ads Python SDK, if the 
        # Bid property is not specified or is set explicitly to None, your keyword bid will not be updated.
        # For examples of how to use the Campaign Management service for keyword updates, please see KeywordsAds.py.
                
        update_bulk_keyword.keyword=update_keyword

        upload_entities=[]

        upload_entities.append(update_bulk_keyword)
                   
        output_status_message("\nUpdating the keyword bid to use the ad group bid . . .")
        download_entities=write_entities_and_upload_file(upload_entities)

        for entity in download_entities:
            if isinstance(entity, BulkKeyword):
                output_bulk_keywords([entity])

        # Here is a simple example that updates the campaign budget.

        download_parameters=DownloadParameters(
            entities=['Budgets Campaigns'],
            result_file_directory=FILE_DIRECTORY,
            result_file_name=DOWNLOAD_FILE_NAME,
            overwrite_result_file=True,
            last_sync_time_in_utc=None
        )

        upload_entities=[]
        get_budget_results=[]
        get_campaign_results=[]

        # Download all campaigns and shared budgets in the account.
        download_entities=download_file(download_parameters)
        output_status_message("Downloaded all campaigns and shared budgets in the account.\n");
        for entity in download_entities:
            if isinstance(entity, BulkBudget):
                get_budget_results.append(entity)
                output_bulk_budgets([entity])
            if isinstance(entity, BulkCampaign):
                get_campaign_results.append(entity)
                output_bulk_campaigns([entity])
        
        # If the campaign has a shared budget you cannot update the Campaign budget amount,
        # and you must instead update the amount in the Budget record. If you try to update 
        # the budget amount of a Campaign that has a shared budget, the service will return 
        # the CampaignServiceCannotUpdateSharedBudget error code.
        for entity in get_budget_results:
            if entity.budget.Id > 0:
                # Increase budget by 20 %
                entity.budget.Amount *= Decimal(1.2)
                upload_entities.append(entity)
        
        for entity in get_campaign_results:
            if entity.campaign.BudgetId == None or entity.campaign.BudgetId <= 0:
                # Increase existing budgets by 20%
                # Monthly budgets are deprecated and there will be a forced migration to daily budgets in calendar year 2017. 
                # Shared budgets do not support the monthly budget type, so this is only applicable to unshared budgets. 
                # During the migration all campaign level unshared budgets will be rationalized as daily. 
                # The formula that will be used to convert monthly to daily budgets is: Monthly budget amount / 30.4.
                # Moving campaign monthly budget to daily budget is encouraged before monthly budgets are migrated. 

                if entity.campaign.BudgetType == 'MonthlyBudgetSpendUntilDepleted':
                    # Increase budget by 20 %
                    entity.campaign.BudgetType = 'DailyBudgetStandard'
                    entity.campaign.DailyBudget = entity.campaign.MonthlyBudget / 30.4 * 1.2
                else:
                    # Increase budget by 20 %
                    entity.campaign.DailyBudget *= 1.2
                upload_entities.append(entity)
                    
        if len(upload_entities) > 0:
            output_status_message("Changed local campaign budget amounts. Starting upload.\n")

            download_entities=write_entities_and_upload_file(upload_entities)       
            for entity in download_entities:
                if isinstance(entity, BulkBudget):
                    get_budget_results.append(entity)
                    output_bulk_budgets([entity])
                if isinstance(entity, BulkCampaign):
                    get_campaign_results.append(entity)
                    output_bulk_campaigns([entity])
        else:
            output_status_message("No campaigns or shared budgets in account.\n")

        # Delete the campaign, ad group, keywords, and ads that were previously added. 
        # You should remove this region if you want to view the added entities in the 
        # Bing Ads web application or another tool.
                
        upload_entities=[]

        for budget_result in budget_results:
            budget_result.status='Deleted'
            upload_entities.append(budget_result)

        for campaign_result in campaign_results:
            campaign_result.campaign.Status='Deleted'
            upload_entities.append(campaign_result)
            
        output_status_message("\nDeleting campaign, budget, ad group, ads, and keywords . . .")
        download_entities=write_entities_and_upload_file(upload_entities)

        for entity in download_entities:
            if isinstance(entity, BulkBudget):
                output_bulk_budgets([entity])
            if isinstance(entity, BulkCampaign):
                output_bulk_campaigns([entity])
            
        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

