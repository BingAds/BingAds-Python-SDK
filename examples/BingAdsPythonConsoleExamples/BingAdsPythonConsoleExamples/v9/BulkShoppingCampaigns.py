from bingads import *
from bingads.bulk import *

import sys
import webbrowser
from time import gmtime, strftime
from suds import WebFault

# Optionally you can include logging to output traffic, for example the SOAP request and response.

#import logging
#logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)ng.getLogger('suds.client').setLevel(logging.DEBUG)

if __name__ == '__main__':
    print("Python loads the web service proxies at runtime, so you will observe " \
          "a performance delay between program launch and main execution...\n")

    ENVIRONMENT='production'
    DEVELOPER_TOKEN='YourDeveloperTokenGoesHere'
    CLIENT_ID='YourClientIdGoesHere'

    CAMPAIGN_ID_KEY=-123
    AD_GROUP_ID_KEY=-1234
    
    FILE_DIRECTORY='c:/bulk/'
    RESULT_FILE_NAME='result.csv'
    UPLOAD_FILE_NAME='upload.csv'
    FILE_TYPE = DownloadFileType.csv

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
        PageInfo = paging,
        Predicates = predicates
    )

def print_percent_complete(progress):
    output_status_message("Percent Complete: {0}\n".format(progress.percent_complete))

def output_status_message(message):
    print(message)

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
            for pair in campaign.ForwardCompatibilityMap:
                output_status_message("Key: {0}".format(pair.Key))
                output_status_message("Value: {0}".format(pair.Value))
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

def output_bulk_ad_groups(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkAdGroup: \n")
        output_status_message("CampaignId: {0}".format(entity.campaign_id))
        output_status_message("CampaignName: {0}".format(entity.campaign_name))
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
        output_status_message("AdRotation Type: {0}".format(
            ad_group.AdRotation.Type if ad_group.AdRotation is not None else None))
        output_status_message("BiddingModel: {0}".format(ad_group.BiddingModel.value))
        output_status_message("BroadMatchBid: {0}".format(
            ad_group.BroadMatchBid.Amount if ad_group.BroadMatchBid is not None else None))
        output_status_message("ContentMatchBid: {0}".format(
            ad_group.ContentMatchBid.Amount if ad_group.ContentMatchBid is not None else None))
        if ad_group.EndDate is not None:
            output_status_message("EndDate: {0}/{1}/{2}".format(
                ad_group.EndDate.Month,
                ad_group.EndDate.Day,
                ad_group.EndDate.Year))
        output_status_message("ExactMatchBid: {0}".format(
            ad_group.ExactMatchBid.Amount if ad_group.ExactMatchBid is not None else None))
        output_status_message("ForwardCompatibilityMap: ")
        if ad_group.ForwardCompatibilityMap is not None and len(ad_group.ForwardCompatibilityMap.KeyValuePairOfstringstring) > 0:
            for pair in campaign.ForwardCompatibilityMap:
                output_status_message("Key: {0}".format(pair.Key))
                output_status_message("Value: {0}".format(pair.Value))
        output_status_message("Id: {0}".format(ad_group.Id))
        output_status_message("Language: {0}".format(ad_group.Language))
        output_status_message("Name: {0}".format(ad_group.Name))
        output_status_message("NativeBidAdjustment: {0}".format(ad_group.NativeBidAdjustment))
        output_status_message("Network: {0}".format(ad_group.Network))
        output_status_message("PhraseMatchBid: {0}".format(
            ad_group.PhraseMatchBid.Amount if ad_group.PhraseMatchBid is not None else None))
        output_status_message("PricingModel: {0}".format(ad_group.PricingModel))
        if ad_group.StartDate is not None:
            output_status_message("StartDate: {0}/{1}/{2}".format(
                ad_group.StartDate.Month,
                ad_group.StartDate.Day,
                ad_group.StartDate.Year))
        output_status_message("Status: {0}".format(ad_group.Status))

def output_bulk_product_ads(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkProductAd: \n")
        output_status_message("AdGroupId: {0}".format(entity.ad_group_id))
        output_status_message("AdGroupName: {0}".format(entity.ad_group_name))
        output_status_message("CampaignName: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        output_bulk_performance_data(entity.performance_data)

        # Output the Campaign Management ProductAd Object
        output_product_ad(entity.ad)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_product_ad(ad):
    if ad is not None:
        output_status_message("AdDistribution: {0}".format(ad.DevicePreference))
        output_status_message("BiddingModel: {0}".format(ad.EditorialStatus))
        output_status_message("ForwardCompatibilityMap: ")
        if ad.ForwardCompatibilityMap is not None and len(ad.ForwardCompatibilityMap.KeyValuePairOfstringstring) > 0:
            for pair in campaign.ForwardCompatibilityMap:
                output_status_message("Key: {0}".format(pair.Key))
                output_status_message("Value: {0}".format(pair.Value))
        output_status_message("Id: {0}".format(ad.Id))
        output_status_message("PromotionalText: {0}".format(ad.PromotionalText))
        output_status_message("Status: {0}".format(ad.Status))

def output_bulk_campaign_product_scopes(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignProductScope: \n")
        output_status_message("CampaignName: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))

        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management CampaignCriterion and ProductScope Objects
        output_campaign_criterion_with_product_scope(entity.campaign_criterion)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_campaign_criterion_with_product_scope(campaign_criterion):
    if campaign_criterion is not None:
        output_status_message("BidAdjustment: {0}".format(campaign_criterion.BidAdjustment))
        output_status_message("CampaignId: {0}".format(campaign_criterion.CampaignId))
        output_status_message("ForwardCompatibilityMap: ")
        if campaign_criterion.ForwardCompatibilityMap is not None and len(campaign_criterion.ForwardCompatibilityMap.KeyValuePairOfstringstring) > 0:
            for pair in campaign_criterion.ForwardCompatibilityMap:
                output_status_message("Key: {0}".format(pair.Key))
                output_status_message("Value: {0}".format(pair.Value))
        output_status_message("CampaignCriterion Id: {0}".format(campaign_criterion.Id))
        output_status_message("CampaignCriterion Type: {0}".format(campaign_criterion.Type))
        
        # Output the Campaign Management ProductScope Object
        output_product_scope(campaign_criterion.Criterion)

def output_product_scope(product_scope):
    if product_scope is not None:
        output_status_message("Product Conditions: ")
        if product_scope.Conditions is not None and len(product_scope.Conditions) > 0:
            for condition in product_scope.Conditions.ProductCondition:
                output_status_message("Operand: {0}".format(condition.Operand))
                output_status_message("Attribute: {0}".format(condition.Attribute))

def output_bulk_ad_group_product_partitions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkAdGroupProductPartition: \n")
        output_status_message("CampaignName: {0}".format(entity.campaign_name))
        output_status_message("AdGroupName: {0}".format(entity.ad_group_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management AdGroupCriterion and ProductPartition Objects
        output_ad_group_criterion_with_product_partition(entity.ad_group_criterion)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_ad_group_criterion_with_product_partition(ad_group_criterion):
    if ad_group_criterion is not None:
        output_status_message("AdGroupId: {0}".format(ad_group_criterion.AdGroupId))
        output_status_message("AdGroupCriterion Id: {0}".format(ad_group_criterion.Id))
        output_status_message("AdGroupCriterion Type: {0}".format(ad_group_criterion.Type))

        if ad_group_criterion.Type == 'BiddableAdGroupCriterion':
            output_status_message("DestinationUrl: {0}".format(ad_group_criterion.DestinationUrl))

            # Output the Campaign Management FixedBid Object
            output_fixed_bid(ad_group_criterion.CriterionBid)
        
        # Output the Campaign Management ProductPartition Object
        output_product_partition(ad_group_criterion.Criterion)

def output_fixed_bid(fixed_bid):
    if fixed_bid is not None and fixed_bid.Bid is not None:
        output_status_message("Bid.Amount: {0}".format(fixed_bid.Bid.Amount))

def output_product_partition(product_partition):
    if product_partition is not None:
        output_status_message("ParentCriterionId: {0}".format(product_partition.ParentCriterionId))
        output_status_message("PartitionType: {0}".format(product_partition.PartitionType))
        if product_partition.Condition is not None:
            output_status_message("Condition: ")
            output_status_message("Operand: {0}".format(product_partition.Condition.Operand))
            output_status_message("Attribute: {0}".format(product_partition.Condition.Attribute))
            
def upload_entities(entities):
    writer=BulkFileWriter(FILE_DIRECTORY+UPLOAD_FILE_NAME);
    for entity in entities:
        writer.write_entity(entity)
    writer.close()

    file_upload_parameters=FileUploadParameters(
        upload_file_path=FILE_DIRECTORY+UPLOAD_FILE_NAME,
        result_file_directory=FILE_DIRECTORY,
        result_file_name=RESULT_FILE_NAME,
        overwrite_result_file=True,
        response_mode='ErrorsAndResults'
    )

    bulk_file_path=bulk_service.upload_file(file_upload_parameters, progress=print_percent_complete)

    with BulkFileReader(file_path=bulk_file_path, result_file_type=ResultFileType.upload, file_format=FILE_TYPE) as reader:
            for entity in reader:
                yield entity

def download_entities(entities):
    download_parameters=DownloadParameters(
        entities=entities,
        result_file_directory=FILE_DIRECTORY,
        result_file_name=RESULT_FILE_NAME,
        overwrite_result_file=True,
        last_sync_time_in_utc=None
    )

    bulk_file_path=bulk_service.download_file(download_parameters, progress=print_percent_complete)

    with BulkFileReader(file_path=bulk_file_path, result_file_type=ResultFileType.full_download, file_format=FILE_TYPE) as reader:
        for entity in reader:
            yield entity

def apply_bulk_product_partition_actions(entities):
    entities=upload_entities(entities)
    
    bulk_ad_group_product_partitions=[]

    for entity in entities:
        if isinstance(entity, BulkAdGroupProductPartition):
            bulk_ad_group_product_partitions.append(entity)
            output_bulk_ad_group_product_partitions([entity])

    return bulk_ad_group_product_partitions

def get_bulk_ad_group_product_partition_tree(ad_group_id):
    entities=['AdGroupProductPartitions']
    downloaded_entities=download_entities(entities)
    
    bulk_ad_group_product_partitions=[]
    
    for entity in downloaded_entities:
        if isinstance(entity, BulkAdGroupProductPartition) and entity.ad_group_criterion is not None and entity.ad_group_criterion.AdGroupId == ad_group_id:
            bulk_ad_group_product_partitions.append(entity)

    return bulk_ad_group_product_partitions

def output_product_partitions(bulk_ad_group_product_partitions):
    """
    Outputs the list of BulkAdGroupProductPartition which each contain an AdGroupCriterion, formatted as a tree. 
    Each AdGroupCriterion must be either a BiddableAdGroupCriterion or NegativeAdGroupCriterion. 

    :param bulk_ad_group_product_partitions: The list of BulkAdGroupProductPartition to output formatted as a tree.
    :type bulk_ad_group_product_partitions: BulkAdGroupProductPartition[]

    """

    # Set up the tree for output

    child_branches={}
    tree_root=None

    for bulk_ad_group_product_partition in bulk_ad_group_product_partitions:
        ad_group_criterion=bulk_ad_group_product_partition.ad_group_criterion
        partition=ad_group_criterion.Criterion
        child_branches[ad_group_criterion.Id]=[]

        # The product partition with ParentCriterionId set to null is the root node.
        if partition.ParentCriterionId is not None:
            child_branches[partition.ParentCriterionId].append(bulk_ad_group_product_partition)
        else:
            tree_root=bulk_ad_group_product_partition

    # Outputs the tree root node and any children recursively
    output_product_partition_tree(tree_root, child_branches, 0)

def output_product_partition_tree(node, child_branches, tree_level):
    """
    Outputs the details of the specified product partition node, 
    and passes any children to itself recursively.

    :param node: The node to output, whether a Subdivision or Unit.
    :type node: BulkAdGroupProductPartition
    :param child_branches: The child branches or nodes if any exist.
    :type child_branches: dict{long, BulkAdGroupProductPartition[]}
    :param tree_level: The number of descendents from the tree root node. 
     Used by this operation to format the tree structure output.
    :type tree_level: int

    """

    if node is None:
        return

    ad_group_criterion=node.ad_group_criterion

    pad=''
    for i in range(0, tree_level):
        pad=pad + '\t'
    output_status_message("{0}{1}".format(
        pad,
        ad_group_criterion.Criterion.PartitionType)
    )

    output_status_message("{0}ParentCriterionId: {1}".format(
        pad,
        ad_group_criterion.Criterion.ParentCriterionId)
    )

    output_status_message("{0}Id: {1}".format(
        pad,
        ad_group_criterion.Id)
    )

    if ad_group_criterion.Criterion.PartitionType == 'Unit':
        if ad_group_criterion.Type == 'BiddableAdGroupCriterion':
            output_status_message("{0}Bid Amount: {1}".format(
                pad,
                ad_group_criterion.CriterionBid.Bid.Amount)
            )
        elif ad_group_criterion.Type == 'NegativeAdGroupCriterion':
            output_status_message("{0}Not Bidding on this Condition".format(
                pad)
            )
           

    null_attribute="(All other)" if ad_group_criterion.Criterion.ParentCriterionId != None else "(Tree Root)"
    output_status_message("{0}Attribute: {1}".format(
        pad,
        null_attribute if ad_group_criterion.Criterion.Condition.Attribute is None else ad_group_criterion.Criterion.Condition.Attribute)
    )

    output_status_message("{0}Operand: {1}\n".format(
        pad,
        ad_group_criterion.Criterion.Condition.Operand)
    )

    for child_node in child_branches[ad_group_criterion.Id]:
        output_product_partition_tree(child_node, child_branches, tree_level + 1)

def get_node_by_client_id(product_partitions, client_id=None):
    """
    Returns the root node of a tree. This operation assumes that a complete 
    product partition tree is provided for one ad group. The node that has
    null ParentCriterionId is the root node.

    :param product_partitions: The list of BulkAdGroupProductPartition that make up the product partition tree.
    :type product_partitions: BulkAdGroupProductPartition[]
    :return: The BulkAdGroupProductPartition corresponding to the specified Client Id.
    :rtype: BulkAdGroupProductPartition

    """

    client_node=None
    for product_partition in product_partitions:
        if product_partition.client_id == client_id:
            client_node=product_partition
            break

    return client_node


class ProductPartitionHelper:
    """ 
    Helper class used to maintain a list of product partition actions for an ad group.
    The list of partition actions can be uploaded to the Bulk service.
    """

    def __init__(self,
                 ad_group_id):
        """ 
        Initialize an instance of this class.

        :param ad_group_id: Each criterion is associated with the same ad group.
        :type ad_group_id: long
        
        """

        self._ad_group_id=ad_group_id
        self._reference_id=-1
        self._partition_actions=[]

    @property
    def partition_actions(self):
        """ 
        The list of BulkAdGroupProductPartition that can be uploaded to the Bulk service

        :rtype: BulkAdGroupProductPartition[]
        """

        return self._partition_actions

    def add_subdivision(self, parent, condition, client_id=None):
        """ 
        Sets the Add action for a new BiddableAdGroupCriterion corresponding to the specified ProductCondition, 
        and adds it to the helper's list of BulkAdGroupProductPartition.

        :param parent: The parent of the product partition subdivision that you want to add.
        :type parent: BulkAdGroupProductPartition
        :param condition: The condition or product filter for the new product partition.
        :type condition: ProductCondition
        :param client_id: The Client Id in the bulk upload file corresponding to the product partition.
        :type client_id: string
        :return: The BulkAdGroupProductPartition that was added to the list of partition_actions.
        :rtype: BulkAdGroupProductPartition
        """

        biddable_ad_group_criterion=campaign_service.factory.create('BiddableAdGroupCriterion')
        product_partition=campaign_service.factory.create('ProductPartition')
        # If the root node is a unit, it would not have a parent
        product_partition.ParentCriterionId=parent.ad_group_criterion.Id if parent != None and parent.ad_group_criterion is not None else None
        product_partition.Condition=condition
        product_partition.PartitionType='Subdivision'
        biddable_ad_group_criterion.Criterion=product_partition
        biddable_ad_group_criterion.CriterionBid=None
        biddable_ad_group_criterion.AdGroupId=self._ad_group_id
        biddable_ad_group_criterion.Status=None
        if hasattr(biddable_ad_group_criterion, 'EditorialStatus'):
            biddable_ad_group_criterion.EditorialStatus=None
        biddable_ad_group_criterion.Id=self._reference_id
        self._reference_id=self._reference_id
        self._reference_id-=1

        # Bids for subdivisions are ignored by Bing Ads.
        # As a workaround to a known Python SDK bug, you can set a FixedBid for the subdivision.
        # The bug is tentatively scheduled to be fixed in early September 2015.
        #fixed_bid=campaign_service.factory.create('FixedBid')
        #biddable_ad_group_criterion.CriterionBid=fixed_bid

        partition_action=BulkAdGroupProductPartition()
        partition_action.client_id=client_id
        partition_action.ad_group_criterion=biddable_ad_group_criterion
        self._partition_actions.append(partition_action)

        return partition_action

    def add_unit(self, parent, condition, bid_amount, is_negative=False, client_id=None):
        """ 
        Sets the Add action for a new AdGroupCriterion corresponding to the specified ProductCondition, 
        and adds it to the helper's list of BulkAdGroupProductPartition.

        :param parent: The parent of the product partition unit that you want to add.
        :type parent: BulkAdGroupProductPartition
        :param condition: The condition or product filter for the new product partition.
        :type condition: ProductCondition
        :param bid_amount: The bid amount for the new product partition.
        :type bid_amount: double
        :param is_negative: (Optional) Indicates whether or not to add a NegativeAdGroupCriterion. 
         The default value is False, in which case a BiddableAdGroupCriterion will be added.
        :type is_negative: bool
        :param client_id: The Client Id in the bulk upload file corresponding to the product partition.
        :type client_id: string
        :return: The BulkAdGroupProductPartition that was added to the list of partition_actions.
        :rtype: BulkAdGroupProductPartition
        """

        ad_group_criterion=None
        if is_negative:
            ad_group_criterion=campaign_service.factory.create('NegativeAdGroupCriterion')
        else:
            ad_group_criterion=campaign_service.factory.create('BiddableAdGroupCriterion')
            fixed_bid=campaign_service.factory.create('FixedBid')
            bid=campaign_service.factory.create('Bid')
            bid.Amount=bid_amount
            fixed_bid.Bid=bid
            ad_group_criterion.CriterionBid=fixed_bid
            
        ad_group_criterion.AdGroupId=self._ad_group_id
        if hasattr(ad_group_criterion, 'EditorialStatus'):
            ad_group_criterion.EditorialStatus=None
        ad_group_criterion.Status=None

        product_partition=campaign_service.factory.create('ProductPartition')
        # If the root node is a unit, it would not have a parent
        product_partition.ParentCriterionId=parent.ad_group_criterion.Id if parent != None and parent.ad_group_criterion is not None else None
        product_partition.Condition=condition
        product_partition.PartitionType='Unit'
        ad_group_criterion.Criterion=product_partition

        partition_action=BulkAdGroupProductPartition()
        partition_action.client_id=client_id
        partition_action.ad_group_criterion=ad_group_criterion
        self._partition_actions.append(partition_action)

        return partition_action

    def delete_partition(self, bulk_ad_group_product_partition):
        """ 
        Sets the Delete action for the specified AdGroupCriterion, 
        and adds it to the helper's list of BulkAdGroupProductPartition.

        :param bulk_ad_group_product_partition: The BulkAdGroupProductPartition whose product partition you want to delete.
        :type bulk_ad_group_product_partition: BulkAdGroupProductPartition
        """

        if bulk_ad_group_product_partition is not None and bulk_ad_group_product_partition.ad_group_criterion is not None:
            bulk_ad_group_product_partition.ad_group_criterion.AdGroupId=self._ad_group_id
            bulk_ad_group_product_partition.ad_group_criterion.Status='Deleted'
            if hasattr(bulk_ad_group_product_partition.ad_group_criterion, 'EditorialStatus'):
                bulk_ad_group_product_partition.ad_group_criterion.EditorialStatus=None
            self._partition_actions.append(bulk_ad_group_product_partition)

    def update_partition(self, bulk_ad_group_product_partition):
        """ 
        Sets the Update action for the specified BiddableAdGroupCriterion, 
        and adds it to the helper's list of BulkAdGroupProductPartition. 
        You can only update the CriterionBid and DestinationUrl elements 
        of the BiddableAdGroupCriterion. 
        When working with product partitions, youu cannot update the Criterion (ProductPartition). 
        To update a ProductPartition, you must delete the existing node (delete_partition) and 
        add a new one (add_unit or add_subdivision) during the same upload.

        :param bulk_ad_group_product_partition: The BulkAdGroupProductPartition to update.
        :type bulk_ad_group_product_partition: BulkAdGroupProductPartition
        """

        if bulk_ad_group_product_partition is not None and bulk_ad_group_product_partition.ad_group_criterion is not None:
            bulk_ad_group_product_partition.ad_group_criterion.AdGroupId=self._ad_group_id
            bulk_ad_group_product_partition.ad_group_criterion.Status=None
            if hasattr(bulk_ad_group_product_partition.ad_group_criterion, 'EditorialStatus'):
                bulk_ad_group_product_partition.ad_group_criterion.EditorialStatus=None
            self._partition_actions.append(bulk_ad_group_product_partition)


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

        # You will need to use the Campaign Management service to get the Bing Merchant Center Store Id. This will be used
        # when creating a new Bing Shopping Campaign.
        # For other operations such as adding product conditions, you can manage Bing Shopping Campaigns solely with the Bulk Service. 

        # Get a list of all Bing Merchant Center stores associated with your CustomerId

        stores=campaign_service.GetBMCStoresByCustomerId()['BMCStore']
        if stores is None:
            output_status_message(
                "You do not have any BMC stores registered for CustomerId {0}.\n".format(authorization_data.customer_id)
            )
            sys.exit(0)

        # Add a new Bing Shopping campaign that will be associated with a ProductScope criterion.
        #  - Set the CampaignType element of the Campaign to Shopping.
        #  - Create a ShoppingSetting instance and set its Priority (0, 1, or 2), SalesCountryCode, and StoreId elements. 
        #    Add this shopping setting to the Settings list of the Campaign.
           
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
	    will be used when associating this new campaign with a new campaign product scope in the BulkCampaignProductScope object below. 
	    '''
        campaign.Id=CAMPAIGN_ID_KEY
        settings=campaign_service.factory.create('ArrayOfSetting')
        setting=campaign_service.factory.create('ShoppingSetting')
        setting.Priority=0
        setting.SalesCountryCode ='US'
        setting.StoreId=stores[0].Id
        settings.Setting.append(setting)
        campaign.Settings=settings
        campaign.CampaignType=['Shopping']
        campaign.Name='Bing Shopping Campaign ' + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description='Bing Shopping Campaign Example.'
        campaign.BudgetType='MonthlyBudgetSpendUntilDepleted'
        campaign.MonthlyBudget=1000
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.DaylightSaving='true' 
        campaign.Status='Paused'
        bulk_campaign.campaign=campaign

        # Optionally, you can create a ProductScope criterion that will be associated with your Bing Shopping campaign. 
        # Use the product scope criterion to include a subset of your product catalog, for example a specific brand, 
        # category, or product type. A campaign can only be associated with one ProductScope, which contains a list 
        # of up to 7 ProductCondition. You'll also be able to specify more specific product conditions for each ad group.

        bulk_campaign_product_scope=BulkCampaignProductScope()
        bulk_campaign_product_scope.status='Active'
        campaign_criterion=campaign_service.factory.create('CampaignCriterion')
        product_scope=campaign_service.factory.create('ProductScope')
        conditions=campaign_service.factory.create('ArrayOfProductCondition')
        condition_new=campaign_service.factory.create('ProductCondition')
        condition_new.Operand='Condition'
        condition_new.Attribute='New'
        conditions.ProductCondition.append(condition_new)
        condition_custom_label_0=campaign_service.factory.create('ProductCondition')
        condition_custom_label_0.Operand='CustomLabel0'
        condition_custom_label_0.Attribute='MerchantDefinedCustomLabel'
        conditions.ProductCondition.append(condition_custom_label_0)
        product_scope.Conditions=conditions
        campaign_criterion.CampaignId=CAMPAIGN_ID_KEY
        campaign_criterion.BidAdjustment=None # Reserved for future use
        campaign_criterion.Criterion=product_scope
        bulk_campaign_product_scope.campaign_criterion=campaign_criterion

        # Specify one or more ad groups.

        bulk_ad_group=BulkAdGroup()
        bulk_ad_group.campaign_id=CAMPAIGN_ID_KEY
        ad_group=campaign_service.factory.create('AdGroup')
        ad_group.Id=AD_GROUP_ID_KEY
        ad_group.Name="Product Categories"
        ad_group.AdDistribution=['Search']
        ad_group.BiddingModel='Keyword'
        ad_group.PricingModel='Cpc'
        ad_group.Network=None
        ad_group.Status='Paused'
        end_date=campaign_service.factory.create('Date')
        end_date.Day=31
        end_date.Month=12
        end_date.Year=2015
        ad_group.EndDate=end_date
        ad_group.Language='English'
        bulk_ad_group.ad_group=ad_group


        #Create a product ad. You must add at least one ProductAd to the corresponding ad group. 
        #A ProductAd is not used directly for delivered ad copy. Instead, the delivery engine generates 
        #product ads from the product details that it finds in your Bing Merchant Center store's product catalog. 
        #The primary purpose of the ProductAd object is to provide promotional text that the delivery engine 
        #adds to the product ads that it generates. For example, if the promotional text is set to 
        #'Free shipping on $99 purchases', the delivery engine will set the product ad's description to 
        #'Free shipping on $99 purchases.'
        
        bulk_product_ad=BulkProductAd()
        bulk_product_ad.ad_group_id=AD_GROUP_ID_KEY
        ads=campaign_service.factory.create('ArrayOfAd')
        product_ad=campaign_service.factory.create('ProductAd')
        product_ad.PromotionalText='Free shipping on $99 purchases.'
        product_ad.Type='Product'
        product_ad.Status=None
        product_ad.EditorialStatus=None
        bulk_product_ad.ad=product_ad
        
        entities=[]
        entities.append(bulk_campaign)
        entities.append(bulk_campaign_product_scope)
        entities.append(bulk_ad_group)
        entities.append(bulk_product_ad)
        
        bulk_entities=upload_entities(entities)
        
        # Write the upload output
        
        campaign_results=[]
        campaign_product_scope_results=[]
        ad_group_results=[]
        product_ad_results=[]

        for entity in bulk_entities:
            if isinstance(entity, BulkCampaign):
                campaign_results.append(entity)
                output_bulk_campaigns([entity])
            if isinstance(entity, BulkCampaignProductScope):
                campaign_product_scope_results.append(entity)
                output_bulk_campaign_product_scopes([entity])
            if isinstance(entity, BulkAdGroup):
                ad_group_results.append(entity)
                output_bulk_ad_groups([entity])
            if isinstance(entity, BulkProductAd):
                product_ad_results.append(entity)
                output_bulk_product_ads([entity])

        ad_group_id=ad_group_results.pop(0).ad_group.Id

        # Bid on all products

        helper=ProductPartitionHelper(ad_group_id)
        
        root_condition=campaign_service.factory.create('ProductCondition')
        root_condition.Operand='All'
        root_condition.Attribute=None

        root=helper.add_unit(
            None,
            root_condition,
            0.35,
            False,
            "root"
        )

        output_status_message("Applying only the root as a Unit with a bid . . . \n")
        apply_bulk_product_partition_actions_results=apply_bulk_product_partition_actions(helper.partition_actions)

        product_partitions=get_bulk_ad_group_product_partition_tree(ad_group_id)

        output_status_message("The ad group's product partition only has a tree root node: \n")
        output_product_partitions(product_partitions)

        # Let's update the bid of the root Unit we just added.

        updated_root=get_node_by_client_id(apply_bulk_product_partition_actions_results, "root")
        fixed_bid=campaign_service.factory.create('FixedBid')
        bid=campaign_service.factory.create('Bid')
        bid.Amount=0.45
        fixed_bid.Bid=bid
        updated_root.ad_group_criterion.CriterionBid=fixed_bid
        
        helper=ProductPartitionHelper(ad_group_id)
        helper.update_partition(updated_root)

        output_status_message("Updating the bid for the tree root node . . . \n")
        apply_bulk_product_partition_actions_results=apply_bulk_product_partition_actions(helper.partition_actions)

        product_partitions=get_bulk_ad_group_product_partition_tree(ad_group_id)

        output_status_message("Updated the bid for the tree root node: \n")
        output_product_partitions(product_partitions)

        
        #Now we will overwrite any existing tree root, and build a product partition group tree structure in multiple steps. 
        #You could build the entire tree in a single call since there are less than 5,000 nodes; however, 
        #we will build it in steps to demonstrate how to use the results from ApplyProductPartitionActions to update the tree. 
        
        #For a list of validation rules, see the Bing Shopping Campaigns technical guide:
        #https://msdn.microsoft.com/en-US/library/bing-ads-campaign-management-bing-shopping-campaigns.aspx
        

        helper=ProductPartitionHelper(ad_group_id)

        #Check whether a root node exists already.

        existing_root=get_node_by_client_id(apply_bulk_product_partition_actions_results, "root")
        if existing_root is not None:
            existing_root.client_id="deletedroot"
            helper.delete_partition(existing_root)

        root_condition=campaign_service.factory.create('ProductCondition')
        root_condition.Operand='All'
        root_condition.Attribute=None
        root=helper.add_subdivision(
            None, 
            root_condition,
            "root"
        )

        
        #The direct children of any node must have the same Operand. 
        #For this example we will use CategoryL1 nodes as children of the root. 
        #For a list of valid CategoryL1 through CategoryL5 values, see the Bing Category Taxonomy:
        #http://advertise.bingads.microsoft.com/en-us/WWDocs/user/search/en-us/Bing_Category_Taxonomy.txt
        
        animals_condition=campaign_service.factory.create('ProductCondition')
        animals_condition.Operand='CategoryL1'
        animals_condition.Attribute='Animals & Pet Supplies'
        animals_subdivision=helper.add_subdivision(
            root,
            animals_condition,
            "animals_subdivision"
        )

        
        #If you use a CategoryL2 node, it must be a descendant (child or later) of a CategoryL1 node. 
        #In other words you cannot have a CategoryL2 node as parent of a CategoryL1 node. 
        #For this example we will a CategoryL2 node as child of the CategoryL1 Animals & Pet Supplies node. 
        
        pet_supplies_condition=campaign_service.factory.create('ProductCondition')
        pet_supplies_condition.Operand='CategoryL2'
        pet_supplies_condition.Attribute='Pet Supplies'
        pet_supplies_subdivision=helper.add_subdivision(
            animals_subdivision,
            pet_supplies_condition,
            "pet_supplies_subdivision"
        )

        brand_a_condition=campaign_service.factory.create('ProductCondition')
        brand_a_condition.Operand='Brand'
        brand_a_condition.Attribute='Brand A'
        brand_a=helper.add_unit(
            pet_supplies_subdivision,
            brand_a_condition,
            0.35,
            False,
            "brand_a"
        )

        
        #If you won't bid on Brand B, set the helper method's bidAmount to '0' and isNegative to True. 
        #The helper method will create a NegativeAdGroupCriterion and apply the condition.
        
        brand_b_condition=campaign_service.factory.create('ProductCondition')
        brand_b_condition.Operand='Brand'
        brand_b_condition.Attribute='Brand B'
        brand_b=helper.add_unit(
            pet_supplies_subdivision,
            brand_b_condition,
            0,
            True,
            "brand_b"
        )

        other_brands_condition=campaign_service.factory.create('ProductCondition')
        other_brands_condition.Operand='Brand'
        other_brands_condition.Attribute=None
        other_brands=helper.add_unit(
            pet_supplies_subdivision,
            other_brands_condition,
            0.35,
            False,
            "other_brands"
        )

        other_pet_supplies_condition=campaign_service.factory.create('ProductCondition')
        other_pet_supplies_condition.Operand='CategoryL2'
        other_pet_supplies_condition.Attribute=None
        other_pet_supplies=helper.add_unit(
            animals_subdivision,
            other_pet_supplies_condition,
            0.35,
            False,
            "other_pet_supplies"
        )

        electronics_condition=campaign_service.factory.create('ProductCondition')
        electronics_condition.Operand='CategoryL1'
        electronics_condition.Attribute='Electronics'
        electronics=helper.add_unit(
            root,
            electronics_condition,
            0.35,
            False,
            "electronics"
        )

        other_categoryL1_condition=campaign_service.factory.create('ProductCondition')
        other_categoryL1_condition.Operand='CategoryL1'
        other_categoryL1_condition.Attribute=None
        other_categoryL1=helper.add_unit(
            root,
            other_categoryL1_condition,
            0.35,
            False,
            "other_categoryL1"
        )

        output_status_message("Applying product partitions to the ad group . . . \n")

        apply_bulk_product_partition_actions_results=apply_bulk_product_partition_actions(helper.partition_actions)

        product_partitions=get_bulk_ad_group_product_partition_tree(ad_group_id)

        
        #The product partition group tree now has 9 nodes. 
                 
        #All other (Root Node)
        #|
        #+-- Animals & Pet Supplies (CategoryL1)
        #|    |
        #|    +-- Pet Supplies (CategoryL2)
        #|    |    |
        #|    |    +-- Brand A
        #|    |    |    
        #|    |    +-- Brand B
        #|    |    |    
        #|    |    +-- All other (Brand)
        #|    |         
        #|    +-- All other (CategoryL2)
        #|        
        #+-- Electronics (CategoryL1)
        #|   
        #+-- All other (CategoryL1)

        output_status_message("The product partition group tree now has 9 nodes: \n")
        output_product_partitions(product_partitions)
        
        
        #Let's replace the Electronics (CategoryL1) node created above with an Electronics (CategoryL1) node that 
        #has children i.e. Brand C (Brand), Brand D (Brand), and All other (Brand) as follows: 
                 
        #Electronics (CategoryL1)
        #|
        #+-- Brand C (Brand)
        #|
        #+-- Brand D (Brand)
        #|
        #+-- All other (Brand)

        helper=ProductPartitionHelper(ad_group_id)

        
        #To replace a node we must know its Id and its ParentCriterionId. In this case the parent of the node 
        #we are replacing is All other (Root Node), and was created at Index 1 of the previous ApplyProductPartitionActions call. 
        #The node that we are replacing is Electronics (CategoryL1), and was created at Index 8. 
        
        root_id=get_node_by_client_id(apply_bulk_product_partition_actions_results, "root").ad_group_criterion.Id
        #electronics.Id=get_node_by_client_id(apply_bulk_product_partition_actions_results, "electronics").ad_group_criterion.Id
        electronics.ad_group_criterion.Id=get_node_by_client_id(apply_bulk_product_partition_actions_results, "electronics").ad_group_criterion.Id
        helper.delete_partition(electronics)

        parent=BulkAdGroupProductPartition()
        parent.ad_group_criterion=campaign_service.factory.create('BiddableAdGroupCriterion')
        parent.ad_group_criterion.Id=root_id

        electronics_subdivision_condition=campaign_service.factory.create('ProductCondition')
        electronics_subdivision_condition.Operand='CategoryL1'
        electronics_subdivision_condition.Attribute='Electronics'
        electronics_subdivision=helper.add_subdivision(
            parent,
            electronics_subdivision_condition,
            "electronics_subdivision"
        )

        brand_c_condition=campaign_service.factory.create('ProductCondition')
        brand_c_condition.Operand='Brand'
        brand_c_condition.Attribute='Brand C'
        brand_c=helper.add_unit(
            electronics_subdivision,
            brand_c_condition,
            0.35,
            False,
            "brand_c"
        )

        brand_d_condition=campaign_service.factory.create('ProductCondition')
        brand_d_condition.Operand='Brand'
        brand_d_condition.Attribute='Brand D'
        brand_d=helper.add_unit(
            electronics_subdivision,
            brand_d_condition,
            0.35,
            False,
            "brand_d"
        )

        other_electronics_brands_condition=campaign_service.factory.create('ProductCondition')
        other_electronics_brands_condition.Operand='Brand'
        other_electronics_brands_condition.Attribute=None
        other_electronics_brands=helper.add_unit(
            electronics_subdivision,
            other_electronics_brands_condition,
            0.35,
            False,
            "other_electronics_brands"
        )

        output_status_message(
            "Updating the product partition group to refine Electronics (CategoryL1) with 3 child nodes . . . \n"
        )
        apply_bulk_product_partition_actions_results=apply_bulk_product_partition_actions(helper.partition_actions)

        product_partitions=get_bulk_ad_group_product_partition_tree(ad_group_id)

        
        #The product partition group tree now has 12 nodes, including the children of Electronics (CategoryL1):
                 
        #All other (Root Node)
        #|
        #+-- Animals & Pet Supplies (CategoryL1)
        #|    |
        #|    +-- Pet Supplies (CategoryL2)
        #|    |    |
        #|    |    +-- Brand A
        #|    |    |    
        #|    |    +-- Brand B
        #|    |    |    
        #|    |    +-- All other (Brand)
        #|    |         
        #|    +-- All other (CategoryL2)
        #|        
        #+-- Electronics (CategoryL1)
        #|    |
        #|    +-- Brand C (Brand)
        #|    |
        #|    +-- Brand D (Brand)
        #|    |
        #|    +-- All other (Brand)
        #|   
        #+-- All other (CategoryL1)        

        output_status_message(
            "The product partition group tree now has 12 nodes, including the children of Electronics (CategoryL1): \n"
        )
        output_product_partitions(product_partitions)

        # Delete the campaign, ad group, criterion, and ad that were previously added. 
        # You should remove this region if you want to view the added entities in the 
        # Bing Ads web application or another tool.
                
        entities=[]
        
        bulk_campaign = BulkCampaign()
        campaign=campaign_service.factory.create('Campaign')
        campaign.Id=campaign_results.pop(0).campaign.Id
        campaign.Status='Deleted'
        bulk_campaign.campaign=campaign
        bulk_campaign.account_id=authorization_data.account_id

        entities.append(bulk_campaign)

        bulk_entities=upload_entities(entities)

        campaign_results=[]

        for entity in bulk_entities:
            if isinstance(entity, BulkCampaign):
                campaign_results.append(entity)
                output_bulk_campaigns([entity])
            
        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

