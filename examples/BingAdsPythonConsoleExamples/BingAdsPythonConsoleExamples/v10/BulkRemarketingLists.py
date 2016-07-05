from bingads.service_client import ServiceClient
from bingads.authorization import *
from bingads.v10 import *
from bingads.v10.bulk import *

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
        output_bidding_scheme(campaign.BiddingScheme)
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
        if ad_group.EndDate is not None:
            output_status_message("EndDate: {0}/{1}/{2}".format(
                ad_group.EndDate.Month,
                ad_group.EndDate.Day,
                ad_group.EndDate.Year))
        output_status_message("ForwardCompatibilityMap: ")
        if ad_group.ForwardCompatibilityMap is not None and len(ad_group.ForwardCompatibilityMap.KeyValuePairOfstringstring) > 0:
            for pair in ad_group.ForwardCompatibilityMap:
                output_status_message("Key: {0}".format(pair.Key))
                output_status_message("Value: {0}".format(pair.Value))
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
        if ad_group.StartDate is not None:
            output_status_message("StartDate: {0}/{1}/{2}".format(
                ad_group.StartDate.Month,
                ad_group.StartDate.Day,
                ad_group.StartDate.Year))
        output_status_message("Status: {0}".format(ad_group.Status))
        output_status_message("TrackingUrlTemplate: {0}".format(ad_group.TrackingUrlTemplate))
        output_status_message("UrlCustomParameters: ")
        if ad_group.UrlCustomParameters is not None and ad_group.UrlCustomParameters.Parameters is not None:
            for custom_parameter in ad_group.UrlCustomParameters.Parameters['CustomParameter']:
                output_status_message("\tKey: {0}".format(custom_parameter.Key))
                output_status_message("\tValue: {0}".format(custom_parameter.Value))

def output_bidding_scheme(bidding_scheme):
    if bidding_scheme is not None:
        output_status_message("BiddingScheme (Bid Strategy Type): {0}".format(bidding_scheme.Type))
        if bidding_scheme.Type == 'MaxClicksBiddingScheme':
            output_status_message("\tMaxCpc: {0}".format(bidding_scheme.MaxCpc))
        elif bidding_scheme.Type == 'MaxConversionsBiddingScheme':
            output_status_message("\tMaxCpc: {0}".format(bidding_scheme.MaxCpc))
            output_status_message("\tStartingBid: {0}".format(bidding_scheme.StartingBid))
        elif bidding_scheme.Type == 'TargetCpaBiddingScheme':
            output_status_message("\tMaxCpc: {0}".format(bidding_scheme.MaxCpc))
            output_status_message("\tStartingBid: {0}".format(bidding_scheme.StartingBid))
            output_status_message("\tTargetCpa: {0}".format(bidding_scheme.TargetCpa))
        else:
            output_status_message("Unknown bidding scheme")

def output_bulk_remarketing_lists(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkRemarketingList: \n")
        output_status_message("Status: {0}".format(entity.status))
        output_status_message("ClientId: {0}".format(entity.client_id))
        
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management RemarketingList Object
        output_remarketing_list(entity.remarketing_list)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_remarketing_list(remarketing_list):
    if remarketing_list is not None:
        output_status_message("Description: {0}".format(remarketing_list.Description))
        output_status_message("ForwardCompatibilityMap: ")
        if remarketing_list.ForwardCompatibilityMap is not None and len(remarketing_list.ForwardCompatibilityMap.KeyValuePairOfstringstring) > 0:
            for pair in remarketing_list.ForwardCompatibilityMap:
                output_status_message("Key: {0}".format(pair.Key))
                output_status_message("Value: {0}".format(pair.Value))
        output_status_message("Id: {0}".format(remarketing_list.Id))
        output_status_message("MembershipDuration: {0}".format(remarketing_list.MembershipDuration))
        output_status_message("Name: {0}".format(remarketing_list.Name))
        output_status_message("ParentId: {0}".format(remarketing_list.ParentId))
        output_status_message("Scope: {0}".format(remarketing_list.Scope))
        output_status_message("TagId: {0}".format(remarketing_list.TagId))

def output_bulk_ad_group_remarketing_lists(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkAdGroupRemarketingList: \n")
        output_status_message("AdGroup Name: {0}".format(entity.ad_group_name))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management AdGroupRemarketingListAssociation Object
        output_ad_group_remarketing_list_association(entity.ad_group_remarketing_list_association)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_ad_group_remarketing_list_association(ad_group_remarketing_list_association):
    if ad_group_remarketing_list_association is not None:
        output_status_message("AdGroupId: {0}".format(ad_group_remarketing_list_association.AdGroupId))
        output_status_message("BidAdjustment: {0}".format(ad_group_remarketing_list_association.BidAdjustment))
        output_status_message("Id: {0}".format(ad_group_remarketing_list_association.Id))
        output_status_message("RemarketingListId: {0}".format(ad_group_remarketing_list_association.RemarketingListId))
        output_status_message("Status: {0}".format(ad_group_remarketing_list_association.Status))

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

        download_parameters=DownloadParameters(
            entities=['RemarketingLists'],
            result_file_directory=FILE_DIRECTORY,
            result_file_name=DOWNLOAD_FILE_NAME,
            overwrite_result_file=True,
            last_sync_time_in_utc=None
        )
        
        download_entities=download_file(download_parameters)
        remarketing_list_results=[]
        output_status_message("Downloaded all remarketing lists that the current user can associate with ad groups.\n");
        for entity in download_entities:
            if isinstance(entity, BulkRemarketingList):
                remarketing_list_results.append(entity)
        
        output_bulk_remarketing_lists(remarketing_list_results)
        
        # You must already have at least one remarketing list. The Bing Ads API does not support
        # remarketing list add, update, or delete operations.
        if remarketing_list_results.count < 1:
            output_status_message("You do not have any remarketing lists that the current user can associate with ad groups.\n")
            sys.exit(0)

        # Prepare the bulk entities that you want to upload. Each bulk entity contains the corresponding campaign management object,  
        # and additional elements needed to read from and write to a bulk file.

        bulk_campaign=BulkCampaign()
        bulk_campaign.client_id='YourClientIdGoesHere'
        campaign=campaign_service.factory.create('Campaign')
        campaign.Id=CAMPAIGN_ID_KEY
        campaign.Name="Summer Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description="Summer shoes line."
        campaign.BudgetType='MonthlyBudgetSpendUntilDepleted'
        campaign.MonthlyBudget=1000
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.Status='Paused'

        # DaylightSaving is not supported in the Bulk file schema. Whether or not you specify it in a BulkCampaign,
        # the value is not written to the Bulk file, and by default DaylightSaving is set to true.
        campaign.DaylightSaving='True'
        
        bulk_campaign.campaign=campaign

        bulk_ad_group=BulkAdGroup()
        
        # The client_id may be used to associate records in the bulk upload file with records in the results file. The value of this field  
        # is not used or stored by the server; it is simply copied from the uploaded record to the corresponding result record. 
        # Note: This bulk file Client Id is not related to an application Client Id for OAuth. 
        
        bulk_ad_group.client_id='YourClientIdGoesHere'
        
        bulk_ad_group.campaign_id=CAMPAIGN_ID_KEY
        ad_group=campaign_service.factory.create('AdGroup')

        # When using the Campaign Management service, the Id cannot be set. In the context of a BulkAdGroup, the Id is optional 
        # and may be used as a negative reference key during bulk upload. For example the same negative value set for the  
        # ad group Id will be used when associating this new ad group with a new ad group remarketing list association
        # in the bulk_ad_group_remarketing_list object below. 
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
        ad_group.TrackingUrlTemplate=None

        # Applicable for all remarketing lists that are associated with this ad group. TargetAndBid indicates 
        # that you want to show ads only to people included in the remarketing list, with the option to change
        # the bid amount. Ads in this ad group will only show to people included in the remarketing list.
        ad_group.RemarketingTargetingSetting='TargetAndBid'

        bulk_ad_group.ad_group=ad_group

        upload_entities=[]
        upload_entities.append(bulk_campaign)
        upload_entities.append(bulk_ad_group)
        
        # This example associates all of the remarketing lists with the new ad group.

        for bulk_remarketing_list in remarketing_list_results:
            if bulk_remarketing_list.remarketing_list != None and bulk_remarketing_list.remarketing_list.Id != None:
                bulk_ad_group_remarketing_list=BulkAdGroupRemarketingList()
                bulk_ad_group_remarketing_list.ClientId = "MyBulkAdGroupRemarketingList " + str(bulk_remarketing_list.remarketing_list.Id)
                ad_group_remarketing_list_association=campaign_service.factory.create('AdGroupRemarketingListAssociation')
                ad_group_remarketing_list_association.AdGroupId=AD_GROUP_ID_KEY
                ad_group_remarketing_list_association.BidAdjustment=90.00
                ad_group_remarketing_list_association.RemarketingListId=bulk_remarketing_list.remarketing_list.Id
                ad_group_remarketing_list_association.Status='Paused'
                bulk_ad_group_remarketing_list.ad_group_remarketing_list_association = ad_group_remarketing_list_association

                upload_entities.append(bulk_ad_group_remarketing_list)
    
        output_status_message("\nAdding campaign, ad group, and ad group remarketing list associations...\n")
        download_entities=write_entities_and_upload_file(upload_entities)

        campaign_results=[]
        ad_group_results=[]
        ad_group_remarketing_list_results=[]

        for entity in download_entities:
            if isinstance(entity, BulkCampaign):
                campaign_results.append(entity)
                output_bulk_campaigns([entity])
            if isinstance(entity, BulkAdGroup):
                ad_group_results.append(entity)
                output_bulk_ad_groups([entity])
            if isinstance(entity, BulkAdGroupRemarketingList):
                ad_group_remarketing_list_results.append([entity])
                output_bulk_ad_group_remarketing_lists([entity])
            

        # Delete the campaign, ad group, and ad group remarketing list associations that were previously added. 
        # The remarketing lists will not be deleted. 
        # You should remove this region if you want to view the added entities in the 
        # Bing Ads web application or another tool.
                
        upload_entities=[]

        for campaign_result in campaign_results:
            campaign_result.campaign.Status='Deleted'
            upload_entities.append(campaign_result)
            
        output_status_message("\nDeleting campaign, ad group, and ad group remarketing list associations . . .")
        download_entities=write_entities_and_upload_file(upload_entities)

        for entity in download_entities:
            if isinstance(entity, BulkCampaign):
                output_bulk_campaigns([entity])
            
        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

