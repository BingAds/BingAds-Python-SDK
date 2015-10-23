from bingads import *
from bingads.bulk import *

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

    CAMPAIGN_ID_KEY=-123
    AD_GROUP_ID_KEY=-1234

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
    campaign.Name="Summer Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    campaign.Description="Summer shoes line."
    campaign.BudgetType='MonthlyBudgetSpendUntilDepleted'
    campaign.MonthlyBudget=1000
    campaign.TimeZone='PacificTimeUSCanadaTijuana'
    campaign.Status='Paused'
    bulk_campaign.campaign=campaign

    return bulk_campaign

def get_sample_bulk_ad_group():
    bulk_ad_group=BulkAdGroup()
    bulk_ad_group.campaign_id=CAMPAIGN_ID_KEY
    ad_group=campaign_service.factory.create('AdGroup')
    ad_group.Id=AD_GROUP_ID_KEY
    ad_group.Name="Women's Red Shoes"
    ad_group.AdDistribution='Search'
    ad_group.BiddingModel='Keyword'
    ad_group.PricingModel='Cpc'
    end_date=campaign_service.factory.create('Date')
    end_date.Day=31
    end_date.Month=12
    end_date.Year=2015
    ad_group.EndDate=end_date
    exact_match_bid=campaign_service.factory.create('Bid')
    exact_match_bid.Amount=0.09
    ad_group.ExactMatchBid=exact_match_bid
    phrase_match_bid=campaign_service.factory.create('Bid')
    phrase_match_bid.Amount=0.07
    ad_group.PhraseMatchBid=phrase_match_bid
    ad_group.Language='English'
    bulk_ad_group.ad_group=ad_group

    return bulk_ad_group

def get_sample_bulk_text_ads():
    # In this example only the second ad should succeed. The Title of the first ad is empty and not valid,
    # and the third ad is a duplicate of the second ad. 

    bulk_text_ads=[]

    for index in range(3):
        bulk_text_ad=BulkTextAd()
        bulk_text_ad.ad_group_id=AD_GROUP_ID_KEY
        text_ad=campaign_service.factory.create('TextAd')
        text_ad.DestinationUrl='http://www.contoso.com/womenshoesale/?season=spring&promocode=PROMO123'
        text_ad.DisplayUrl='Contoso.com'
        text_ad.Text='Huge Savings on red shoes.'
        text_ad.Title='Red Shoe Sale'
        text_ad.Type='Text'
        text_ad.Status=None
        text_ad.EditorialStatus=None
        bulk_text_ad.ad=text_ad
        bulk_text_ads.append(bulk_text_ad)

    bulk_text_ads[0].ad.Title=''

    return bulk_text_ads

def get_sample_bulk_keywords():
    # In this example only the second keyword should succeed. The Text of the first keyword exceeds the limit,
    # and the third keyword is a duplicate of the second keyword. 
	
    bulk_keywords=[]

    for index in range(3):
        bulk_keyword=BulkKeyword()
        bulk_keyword.ad_group_id=AD_GROUP_ID_KEY
        keyword=campaign_service.factory.create('Keyword')
        keyword.Bid.Amount=0.47
        keyword.Param2='10% Off'
        keyword.MatchType='Broad'
        keyword.Text='Brand-A Shoes'
        bulk_keyword.keyword=keyword
        bulk_keywords.append(bulk_keyword)

    bulk_keywords[0].keyword.Text=(
        "Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes "
		"Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes "
		"Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes"
    )

    return bulk_keywords

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
        output_status_message("AdGroup Name: {0}".format(entity.ad_group.Name))
        output_status_message("AdGroup Id: {0}".format(entity.ad_group.Id))

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_text_ads(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkTextAd: \n")
        output_status_message("TextAd DisplayUrl: {0}".format(entity.ad.DisplayUrl))
        output_status_message("TextAd Title: {0}".format(entity.ad.Title))
        output_status_message("TextAd Id: {0}".format(entity.ad.Id))

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_keywords(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkKeyword: \n")
        output_status_message("Keyword Text: {0}".format(entity.keyword.Text))
        output_status_message("Keyword Id: {0}".format(entity.keyword.Id))
         
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
        user_id=None
        user=customer_service.GetUser(None).User
        accounts=search_accounts_by_user_id(user.Id)
        
        # For this example we'll use the first account.
        authorization_data.account_id=accounts['Account'][0].Id
        authorization_data.customer_id=accounts['Account'][0].ParentCustomerId

        # Prepare the bulk entities that you want to upload. Each bulk entity contains the corresponding campaign management object,  
        # and additional elements needed to read from and write to a bulk file.

        bulk_campaign=get_sample_bulk_campaign()
        bulk_ad_group=get_sample_bulk_ad_group()
        bulk_text_ads=get_sample_bulk_text_ads()
        bulk_keywords=get_sample_bulk_keywords()
    
        # Write the entities created above, to temporary memory. 
        # Dependent entities such as BulkKeyword must be written after any dependencies,   
        # for example the BulkCampaign and BulkAdGroup. 

        upload_entities=[]
        upload_entities.append(bulk_campaign)
        upload_entities.append(bulk_ad_group)
        for bulk_text_ad in bulk_text_ads:
            upload_entities.append(bulk_text_ad)
        for bulk_keyword in bulk_keywords:
            upload_entities.append(bulk_keyword)      
        
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
            if isinstance(entity, BulkAdGroup):
                output_bulk_ad_groups([entity])
            if isinstance(entity, BulkTextAd):
                output_bulk_text_ads([entity])
            if isinstance(entity, BulkKeyword):
                output_bulk_keywords([entity])

        # Complete a full download of all campaigns, ad groups, ads, and keywords in the account. 
        # This download will include any entities successfully added above.

        download_parameters=DownloadParameters(
            result_file_directory=FILE_DIRECTORY, 
            result_file_name=RESULT_FILE_NAME, 
            overwrite_result_file=True, # Set this value true if you want to overwrite the same file.
            data_scope=[ 'EntityData' ],
            entities=[ 'Campaigns', 'AdGroups', 'Keywords', 'Ads' ],
            file_type='Csv',
            campaign_ids=None,
            last_sync_time_in_utc=None,
            location_target_version=None,
            performance_stats_date_range=None
        )

        output_status_message("Starting download_entities . . .")

        bulk_entities=bulk_service.download_entities(download_parameters, progress=None)

        output_status_message("Printing the results of download_entities . . .")

        for entity in bulk_entities:
            if isinstance(entity, BulkCampaign):
                output_bulk_campaigns([entity])
            if isinstance(entity, BulkAdGroup):
                output_bulk_ad_groups([entity])
            if isinstance(entity, BulkTextAd):
                output_bulk_text_ads([entity])
            if isinstance(entity, BulkKeyword):
                output_bulk_keywords([entity])

        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

