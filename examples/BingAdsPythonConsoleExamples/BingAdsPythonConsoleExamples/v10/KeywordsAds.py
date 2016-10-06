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

def set_read_only_campaign_elements_to_none(campaign):
    if campaign is not None:
        campaign.CampaignType=None
        campaign.Settings=None
        campaign.Status=None

def output_campaign(campaign):
    if campaign is not None:
        if hasattr(campaign, 'BiddingScheme'): 
            output_bidding_scheme(campaign.BiddingScheme)
        if hasattr(campaign, 'BudgetId'): 
            output_status_message("BudgetId: {0}".format(campaign.BudgetId))
        output_status_message("BudgetType: {0}".format(campaign.BudgetType))
        output_status_message("CampaignType: {0}".format(campaign.CampaignType))
        output_status_message("DailyBudget: {0}".format(campaign.DailyBudget))
        output_status_message("Description: {0}".format(campaign.Description))
        output_status_message("ForwardCompatibilityMap: ");
        if campaign.ForwardCompatibilityMap is not None:
            for pair in campaign.ForwardCompatibilityMap['KeyValuePairOfstringstring']:
                output_status_message("Key: {0}".format(pair.key))
                output_status_message("Value: {0}".format(pair.value))
        output_status_message("Id: {0}".format(campaign.Id))
        output_status_message("MonthlyBudget: {0}".format(campaign.MonthlyBudget))
        output_status_message("Name: {0}".format(campaign.Name))
        output_status_message("Settings:");
        if campaign.Settings is not None:
            for setting in campaign.Settings['Setting']:
                if setting.Type == 'ShoppingSetting':
                    output_status_message("ShoppingSetting:");
                    output_status_message("Priority: {0}".format(setting.Priority))
                    output_status_message("SalesCountryCode: {0}".format(setting.SalesCountryCode))
                    output_status_message("StoreId: {0}".format(setting.StoreId))
        output_status_message("Status: {0}".format(campaign.Status))
        output_status_message("TrackingUrlTemplate: {0}".format(campaign.TrackingUrlTemplate))
        output_status_message("UrlCustomParameters: ");
        if campaign.UrlCustomParameters is not None and campaign.UrlCustomParameters.Parameters is not None:
            for custom_parameter in campaign.UrlCustomParameters.Parameters['CustomParameter']:
                output_status_message("\tKey: {0}".format(custom_parameter.Key))
                output_status_message("\tValue: {0}".format(custom_parameter.Value))
        output_status_message("TimeZone: {0}\n".format(campaign.TimeZone))

def output_bidding_scheme(bidding_scheme):
    if bidding_scheme is None:
        return
    if bidding_scheme.Type == 'EnhancedCpc':
        output_status_message("BiddingScheme Type: EnhancedCpc")
    elif bidding_scheme.Type == 'InheritFromParent':
        output_status_message("BiddingScheme Type: InheritFromParent")
    elif bidding_scheme.Type == 'ManualCpc':
        output_status_message("BiddingScheme Type: ManualCpc")
    elif bidding_scheme.Type == 'MaxClicks':
        output_status_message("BiddingScheme Type: MaxClicks")
    elif bidding_scheme.Type == 'MaxConversions':
        output_status_message("BiddingScheme Type: MaxConversions")
    elif bidding_scheme.Type == 'TargetCpa':
        output_status_message("BiddingScheme Type: TargetCpa")

def output_budget(budget):
    if budget is not None:
        output_status_message("Amount: {0}".format(budget.Amount))
        output_status_message("AssociationCount: {0}".format(budget.AssociationCount))
        output_status_message("BudgetType: {0}".format(budget.BudgetType))
        output_status_message("Id: {0}".format(budget.Id))
        output_status_message("Name: {0}\n".format(budget.Name))
    
def output_campaign_ids(campaign_ids):
    for id in campaign_ids['long']:
        output_status_message("Campaign successfully added and assigned CampaignId {0}\n".format(id))

def output_ad_group_ids(ad_group_ids):
    for id in ad_group_ids['long']:
        output_status_message("AdGroup successfully added and assigned AdGroupId {0}\n".format(id))

def output_ad_results(ads, ad_ids, ad_errors):
    # Since len(ads['Ad']) and len(ad_errors['long']) usually differ, we will need to adjust the ad_errors index 
    # as successful indices are counted. 
    success_count=0 

    # There is an issue in the SUDS 0.6 library, where if Index 0 of ArrayOfNullableOflong is empty it is not returned. 
    # In this case we will need to adjust the index used to access ad_ids.
    suds_index_0_gap=len(ads['Ad']) - len(ad_ids['long'])

    error_index=0

    for ad_index in range(len(ads['Ad'])):
        attribute_value=None
        if ads['Ad'][ad_index].Type == 'Text':
            attribute_value="Title: {0}".format(ads['Ad'][ad_index].Title)
        elif ads['Ad'][ad_index].Type == 'Product':
            attribute_value="PromotionalText: {0}".format(ads['Ad'][ad_index].PromotionalText)
        else:
            attribute_value="Unknown Ad Type"
        
        if ad_errors is not None \
            and ad_errors['BatchError'] is not None \
            and ad_index < len(ad_errors['BatchError']) + success_count \
            and ad_index == ad_errors['BatchError'][error_index].Index:
            # One ad may have multiple errors, for example editorial errors in multiple publisher countries
            while(error_index < len(ad_errors['BatchError']) and ad_errors['BatchError'][error_index].Index == ad_index):
                output_status_message("Ad[{0}] ({1}) not added due to the following error:".format(ad_index, attribute_value))
                output_status_message("Index: {0}".format(ad_errors['BatchError'][error_index].Index))
                output_status_message("Code: {0}".format(ad_errors['BatchError'][error_index].Code))
                output_status_message("ErrorCode: {0}".format(ad_errors['BatchError'][error_index].ErrorCode))
                output_status_message("Message: {0}".format(ad_errors['BatchError'][error_index].Message))
                if ad_errors['BatchError'][error_index].Type == 'EditorialError':
                    output_status_message("DisapprovedText: {0}".format(ad_errors['BatchError'][error_index].DisapprovedText)) 
                    output_status_message("Location: {0}".format(ad_errors['BatchError'][error_index].Location)) 
                    output_status_message("PublisherCountry: {0}".format(ad_errors['BatchError'][error_index].PublisherCountry)) 
                    output_status_message("ReasonCode: {0}".format(ad_errors['BatchError'][error_index].ReasonCode)) 
                error_index=error_index + 1
        elif ad_ids['long'][ad_index - suds_index_0_gap] is not None:
            output_status_message("Ad[{0}] ({1}) successfully added and assigned AdId {2}".format( 
                        ad_index,
                        attribute_value,
                        ad_ids['long'][ad_index - suds_index_0_gap]))
            success_count=success_count + 1
        output_status_message('')

def output_keyword_results(keywords, keyword_ids, keyword_errors):
    # Since len(keywords['Keyword']) and len(keyword_errors['long']) differ, we will need to adjust the keyword_errors index 
    # as successful indices are counted. 
    success_count=0 

    # There is an issue in the SUDS 0.6 library, where if Index 0 of ArrayOfNullableOflong is empty it is not returned. 
    # In this case we will need to adjust the index used to access keyword_ids.
    suds_index_0_gap=len(keywords['Keyword']) - len(keyword_ids['long'])

    error_index=0
    
    for keyword_index in range(len(keywords['Keyword'])):
        attribute_value=keywords['Keyword'][keyword_index].Text
        
        if keyword_errors \
            and keyword_index < len(keyword_errors['BatchError']) + success_count \
            and keyword_index == keyword_errors['BatchError'][error_index].Index:
            # One keyword may have multiple errors, for example editorial errors in multiple publisher countries
            while(error_index < len(keyword_errors['BatchError']) and keyword_errors['BatchError'][error_index].Index == keyword_index):
                output_status_message("Keyword[{0}] ({1}) not added due to the following error:".format(keyword_index, attribute_value))
                output_status_message("Index: {0}".format(keyword_errors['BatchError'][error_index].Index))
                output_status_message("Code: {0}".format(keyword_errors['BatchError'][error_index].Code))
                output_status_message("ErrorCode: {0}".format(keyword_errors['BatchError'][error_index].ErrorCode))
                output_status_message("Message: {0}".format(keyword_errors['BatchError'][error_index].Message))
                if keyword_errors['BatchError'][error_index].Type == 'EditorialError':
                    output_status_message("DisapprovedText: {0}".format(keyword_errors['BatchError'][error_index].DisapprovedText)) 
                    output_status_message("Location: {0}".format(keyword_errors['BatchError'][error_index].Location)) 
                    output_status_message("PublisherCountry: {0}".format(keyword_errors['BatchError'][error_index].PublisherCountry)) 
                    output_status_message("ReasonCode: {0}".format(keyword_errors['BatchError'][error_index].ReasonCode)) 
                error_index=error_index + 1
        elif keyword_ids['long'][keyword_index - suds_index_0_gap] is not None:
            output_status_message("Keyword[{0}] ({1}) successfully added and assigned KeywordId {2}".format( 
                        keyword_index,
                        attribute_value,
                        keyword_ids['long'][keyword_index - suds_index_0_gap]))
            success_count=success_count + 1
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

        # Determine whether you are able to add shared budgets by checking the pilot flags.

        enabled_for_shared_budgets = False
        feature_pilot_flags = customer_service.GetCustomerPilotFeatures(authorization_data.customer_id)

        # The pilot flag value for shared budgets is 263.
        # Pilot flags apply to all accounts within a given customer.
        if(263 in feature_pilot_flags['int']):
            enabled_for_shared_budgets = True
        
        # If the customer is enabled for shared budgets, let's create a new budget and
        # share it with a new campaign.

        budget_ids = None
        if enabled_for_shared_budgets:
            budgets = campaign_service.factory.create('ArrayOfBudget')
            budget=set_elements_to_none(campaign_service.factory.create('Budget'))
            budget.Amount = 50
            budget.BudgetType = 'DailyBudgetStandard'
            budget.Name = "My Shared Budget " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
            budgets.Budget.append(budget)
                    
            add_budgets_response = campaign_service.AddBudgets(budgets)
            budget_ids={
                'long': add_budgets_response.BudgetIds['long'] if add_budgets_response.BudgetIds['long'] else None
            }

        # Specify one or more campaigns.
        
        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.Name="Summer Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description="Summer shoes line."

        # You must choose to set either the shared  budget ID or daily amount.
        # You can set one or the other, but you may not set both.
        campaign.BudgetId = budget_ids['long'][0] if enabled_for_shared_budgets else None
        campaign.DailyBudget = None if enabled_for_shared_budgets else 50
        campaign.BudgetType = 'DailyBudgetStandard'

        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.DaylightSaving=True # Accepts 'true','false', True, or False
        campaign.Status='Paused'

        # You can set your campaign bid strategy to Enhanced CPC (EnhancedCpcBiddingScheme) 
        # and then, at any time, set an individual ad group or keyword bid strategy to 
        # Manual CPC (ManualCpcBiddingScheme).
        # For campaigns you can use either of the EnhancedCpcBiddingScheme or ManualCpcBiddingScheme objects. 
        # If you do not set this element, then ManualCpcBiddingScheme is used by default.
        campaign_bidding_scheme=set_elements_to_none(campaign_service.factory.create('ns0:EnhancedCpcBiddingScheme'))
        campaign.BiddingScheme=campaign_bidding_scheme

        # Used with FinalUrls shown in the text ads that we will add below.
        campaign.TrackingUrlTemplate="http://tracker.example.com/?season={_season}&promocode={_promocode}&u={lpurl}"
        
        campaigns.Campaign.append(campaign)

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
        ad_group.RemarketingTargetingSetting='TargetAndBid'
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

        ad_groups.AdGroup.append(ad_group)

        # In this example only the first 3 ads should succeed. 
        # The Title of the fourth ad is empty and not valid,
        # and the fifth ad is a duplicate of the second ad.
        
        ads=campaign_service.factory.create('ArrayOfAd')
        
        for index in range(5):
            text_ad=set_elements_to_none(campaign_service.factory.create('TextAd'))
            text_ad.Title='Red Shoe Sale'
            text_ad.Text='Huge Savings on red shoes.'
            text_ad.DisplayUrl='Contoso.com'
            text_ad.Type='Text'

            # If you are currently using the Destination URL, you must upgrade to Final URLs. 
            # Here is an example of a DestinationUrl you might have used previously. 
            # text_ad.DestinationUrl='http://www.contoso.com/womenshoesale/?season=spring&promocode=PROMO123'

            # To migrate from DestinationUrl to FinalUrls for existing ads, you can set DestinationUrl
            # to an empty string when updating the ad. If you are removing DestinationUrl,
            # then FinalUrls is required.
            # text_ad.DestinationUrl=""
            
            # With FinalUrls you can separate the tracking template, custom parameters, and 
            # landing page URLs.
            final_urls=campaign_service.factory.create('ns4:ArrayOfstring')
            final_urls.string.append('http://www.contoso.com/womenshoesale')
            text_ad.FinalUrls=final_urls

            # Final Mobile URLs can also be used if you want to direct the user to a different page 
            # for mobile devices.
            final_mobile_urls=campaign_service.factory.create('ns4:ArrayOfstring')
            final_mobile_urls.string.append('http://mobile.contoso.com/womenshoesale')
            text_ad.FinalMobileUrls=final_mobile_urls

            # You could use a tracking template which would override the campaign level
            # tracking template. Tracking templates defined for lower level entities 
            # override those set for higher level entities.
            # In this example we are using the campaign level tracking template.
            text_ad.TrackingUrlTemplate=None,

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
            text_ad.UrlCustomParameters=url_custom_parameters
            ads.Ad.append(text_ad)
        
        ads.Ad[0].Title="Women's Shoe Sale"
        ads.Ad[1].Title="Women's Super Shoe Sale"
        ads.Ad[2].Title="Women's Red Shoe Sale"
        ads.Ad[3].Title=''
        ads.Ad[4].Title="Women's Super Shoe Sale"

        # In this example only the second keyword should succeed. The Text of the first keyword exceeds the limit,
        # and the third keyword is a duplicate of the second keyword.  

        keywords=campaign_service.factory.create('ArrayOfKeyword')
        
        for index in range(3):
            keyword=set_elements_to_none(campaign_service.factory.create('Keyword'))
            keyword.Bid=campaign_service.factory.create('Bid')
            keyword.Bid.Amount=0.47
            keyword.Param2='10% Off'
            keyword.MatchType='Broad'
            keyword.Text='Brand-A Shoes'

            # For keywords you can use either of the InheritFromParentBiddingScheme or ManualCpcBiddingScheme objects. 
            # If you do not set this element, then InheritFromParentBiddingScheme is used by default.
            keyword_bidding_scheme=set_elements_to_none(campaign_service.factory.create('ns0:InheritFromParentBiddingScheme'))
            keyword.BiddingScheme=keyword_bidding_scheme

            keywords.Keyword.append(keyword)
        
        keywords.Keyword[0].Text=(
            "Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes "
		    "Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes "
		    "Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes Brand-A Shoes"
        )

        # Add the campaign, ad group, keywords, and ads
        
        add_campaigns_response=campaign_service.AddCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=campaigns
        )
        campaign_ids={
            'long': add_campaigns_response.CampaignIds['long'] if add_campaigns_response.CampaignIds['long'] else None
        }
        output_campaign_ids(campaign_ids)
        
        add_ad_groups_response=campaign_service.AddAdGroups(
            CampaignId=campaign_ids['long'][0],
            AdGroups=ad_groups
        )
        ad_group_ids={
            'long': add_ad_groups_response.AdGroupIds['long'] if add_ad_groups_response.AdGroupIds['long'] else None
        }
        output_ad_group_ids(ad_group_ids)
        
        add_ads_response=campaign_service.AddAds(
            AdGroupId=ad_group_ids['long'][0],
            Ads=ads
        )
        ad_ids={
            'long': add_ads_response.AdIds['long'] if add_ads_response.AdIds['long'] else None
        }
        ad_errors={
            'BatchError': add_ads_response.PartialErrors['BatchError'] if add_ads_response.PartialErrors else None
        }    
        output_ad_results(ads, ad_ids, ad_errors)
        
        add_keywords_response=campaign_service.AddKeywords(
            AdGroupId=ad_group_ids['long'][0],
            Keywords=keywords
        )
        keyword_ids={
            'long': add_keywords_response.KeywordIds['long'] if add_keywords_response.KeywordIds else None
        }
        keyword_errors={
            'BatchError': add_keywords_response.PartialErrors['BatchError'] if add_keywords_response.PartialErrors else None
        } 
    
        output_keyword_results(keywords, keyword_ids, keyword_errors)
        
        # Here is a simple example that updates the campaign budget.
        # If the campaign has a shared budget you cannot update the Campaign budget amount,
        # and you must instead update the amount in the Budget object. If you try to update 
        # the budget amount of a campaign that has a shared budget, the service will return 
        # the CampaignServiceCannotUpdateSharedBudget error code.

        get_campaigns=campaign_service.GetCampaignsByAccountId(
            AccountId=authorization_data.account_id,
            CampaignType=['SearchAndContent Shopping'],
            ReturnAdditionalFields=['BiddingScheme BudgetId']
        )
        
        update_campaigns = campaign_service.factory.create('ArrayOfCampaign')
        update_budgets = campaign_service.factory.create('ArrayOfBudget')
        get_campaign_ids = []
        get_budget_ids = []

        # Increase existing budgets by 20%
        for campaign in get_campaigns['Campaign']:

            # If the campaign has a shared budget, let's add the budget ID to the list we will update later.
            if campaign is not None and hasattr(campaign, 'BudgetId') and campaign.BudgetId > 0:
                get_budget_ids.append(campaign.BudgetId)
            # If the campaign has its own budget, let's add it to the list of campaigns to update later.
            elif campaign is not None:
                update_campaigns.Campaign.append(campaign)
        
        # Update shared budgets in Budget objects.
        if get_budget_ids is not None and len(get_budget_ids) > 0:
            distinct_budget_ids = {'long': list(set(get_budget_ids))}
            get_budgets = campaign_service.GetBudgetsByIds(
                BudgetIds=distinct_budget_ids
            ).Budgets

            output_status_message("List of shared budgets BEFORE update:\n")
            for budget in get_budgets['Budget']:
                output_status_message("Budget:")
                output_budget(budget)

            output_status_message("List of campaigns that share each budget:\n");
            get_campaign_id_collection = campaign_service.GetCampaignIdsByBudgetIds(distinct_budget_ids).CampaignIdCollection

            index=0

            for index in range(len(get_campaign_id_collection['IdCollection'])):
                output_status_message("BudgetId: {0}".format(distinct_budget_ids['long'][index]))
                output_status_message("Campaign Ids:");
                if get_campaign_id_collection['IdCollection'][index] is not None:
                    for id in get_campaign_id_collection['IdCollection'][index].Ids['long']:
                        output_status_message("\t{0}".format(id))
                index=index+1

            for budget in get_budgets['Budget']:
                if budget is not None:
                    # Increase budget by 20 %
                    budget.Amount *= 1.2
                    update_budgets.Budget.append(budget)
            campaign_service.UpdateBudgets(Budgets=update_budgets)

            get_budgets = campaign_service.GetBudgetsByIds(
                BudgetIds=distinct_budget_ids
            ).Budgets

            output_status_message("List of shared budgets AFTER update:\n");
            for budget in get_budgets['Budget']:
                output_status_message("Budget:")
                output_budget(budget)

        # Update unshared budgets in Campaign objects.
        if update_campaigns is not None:

            # The UpdateCampaigns operation only accepts 100 Campaign objects per call. 
            # To simply the example we will update the first 100.
            update_100_campaigns = update_campaigns['Campaign'][:100]
            update_campaigns = campaign_service.factory.create('ArrayOfCampaign')
            for campaign in update_100_campaigns:
                update_campaigns.Campaign.append(campaign)

            output_status_message("List of campaigns with unshared budget BEFORE budget update:\n");
            for campaign in update_campaigns['Campaign']:
                output_status_message("Campaign:");
                output_campaign(campaign)
                set_read_only_campaign_elements_to_none(campaign)

                # Monthly budgets are deprecated and there will be a forced migration to daily budgets in calendar year 2017. 
                # Shared budgets do not support the monthly budget type, so this is only applicable to unshared budgets. 
                # During the migration all campaign level unshared budgets will be rationalized as daily. 
                # The formula that will be used to convert monthly to daily budgets is: Monthly budget amount / 30.4.
                # Moving campaign monthly budget to daily budget is encouraged before monthly budgets are migrated. 

                if campaign.BudgetType == 'MonthlyBudgetSpendUntilDepleted':
                    # Increase budget by 20 %
                    campaign.BudgetType = 'DailyBudgetStandard'
                    campaign.DailyBudget = (campaign.MonthlyBudget / 30.4) * 1.2
                else:
                    # Increase budget by 20 %
                    campaign.DailyBudget *= 1.2

                get_campaign_ids.append(campaign.Id)
            
            campaign_service.UpdateCampaigns(
                AccountId=authorization_data.account_id,
                Campaigns=update_campaigns
            );

            get_campaigns=campaign_service.GetCampaignsByIds(
                AccountId=authorization_data.account_id,
                CampaignIds={'long': get_campaign_ids},
                CampaignType=['SearchAndContent Shopping'],
                ReturnAdditionalFields=['BiddingScheme BudgetId']
            ).Campaigns
            
            output_status_message("List of campaigns with unshared budget AFTER budget update:\n");
            for campaign in get_campaigns['Campaign']:
                output_status_message("Campaign:");
                output_campaign(campaign)
        
        # Update the Text for the 3 successfully created ads, and update some UrlCustomParameters.
        update_ads=campaign_service.factory.create('ArrayOfAd')

        # Set the UrlCustomParameters element to null or empty to retain any 
        # existing custom parameters.
        text_ad_0=set_elements_to_none(campaign_service.factory.create('TextAd'))
        text_ad_0.Id=ad_ids['long'][0]
        text_ad_0.Text='Huge Savings on All Red Shoes.'
        text_ad_0.UrlCustomParameters=None
        text_ad_0.Type='Text'
        update_ads.Ad.append(text_ad_0)

        # To remove all custom parameters, set the Parameters element of the 
        # CustomParameters object to null or empty.
        text_ad_1=set_elements_to_none(campaign_service.factory.create('TextAd'))
        text_ad_1.Id=ad_ids['long'][1]
        text_ad_1.Text='Huge Savings on All Red Shoes.'
        url_custom_parameters_1=campaign_service.factory.create('ns0:CustomParameters')
        parameters_1=campaign_service.factory.create('ns0:ArrayOfCustomParameter')
        custom_parameter_1=campaign_service.factory.create('ns0:CustomParameter')
        # Set the CustomParameter to None or leave unspecified to have the same effect
        #custom_parameter_1=None
        parameters_1.CustomParameter.append(custom_parameter_1)
        url_custom_parameters_1.Parameters=parameters_1
        text_ad_1.UrlCustomParameters=url_custom_parameters_1
        text_ad_1.Type='Text'
        update_ads.Ad.append(text_ad_1)

        # To remove a subset of custom parameters, specify the custom parameters that 
        # you want to keep in the Parameters element of the CustomParameters object.
        text_ad_2=set_elements_to_none(campaign_service.factory.create('TextAd'))
        text_ad_2.Id=ad_ids['long'][2]
        text_ad_2.Text='Huge Savings on All Red Shoes.'
        url_custom_parameters_2=campaign_service.factory.create('ns0:CustomParameters')
        parameters_2=campaign_service.factory.create('ns0:ArrayOfCustomParameter')
        custom_parameter_2=campaign_service.factory.create('ns0:CustomParameter')
        custom_parameter_2.Key='promoCode'
        custom_parameter_2.Value='updatedpromo'
        parameters_2.CustomParameter.append(custom_parameter_2)
        url_custom_parameters_2.Parameters=parameters_2
        text_ad_2.UrlCustomParameters=url_custom_parameters_2
        text_ad_2.Type='Text'
        update_ads.Ad.append(text_ad_2)

        # As an exercise you can step through using the debugger and view the results.

        campaign_service.GetAdsByAdGroupId(
            AdGroupId=ad_group_ids['long'][0],
            AdTypes=None
        )
        campaign_service.UpdateAds(
            AdGroupId=ad_group_ids['long'][0],
            Ads=update_ads
        )
        campaign_service.GetAdsByAdGroupId(
            AdGroupId=ad_group_ids['long'][0],
            AdTypes=None
        )

        update_keywords=campaign_service.factory.create('ArrayOfKeyword')
        update_keyword=set_elements_to_none(campaign_service.factory.create('Keyword'))
        update_keyword.Id=keyword_ids['long'][0]
        
        # You can set the Bid.Amount property to change the keyword level bid.
        update_keyword.Bid=campaign_service.factory.create('Bid')
        update_keyword.Bid.Amount=0.46
        
        # When using the Campaign Management service with the Bing Ads Python SDK,
        # if you want to inherit the ad group level bid, instead of using the keyword level bid,
        # the service expects that you would have set the Bid.Amount null (new empty Bid). However, 
        # it is important to note that SUDS (used by the Bing Ads Python SDK) does not allow the 
        # Bid.Amount property to be null, so you will need to delete the keyword and then add a new 
        # keyword without the Bid set, or with Bid set to None. 

        # We recommend that you use the BulkServiceManager for keyword updates, i.e. upload BulkKeyword entities.
        # With the BulkKeyword upload, you won't have to delete and add keywords to inherit from the ad group level bid,
        # and you also have the flexibility of updating millions of keywords across all campaigns in your account.
        # For examples of how to use the Bulk service for keyword updates, please see BulkKeywordsAds.py.
        
        # When using the Campaign Management service with the Bing Ads Python SDK,
        # if the Bid property is not specified or is null, your keyword bid will not be updated.
        #update_keyword.Bid=None
        
        update_keywords.Keyword.append(update_keyword)

        campaign_service.GetKeywordsByAdGroupId(
            AdGroupId=ad_group_ids['long'][0],
            ReturnAdditionalFields=['BiddingScheme']
        )
        campaign_service.UpdateKeywords(
            AdGroupId=ad_group_ids['long'][0],
            Keywords=update_keywords
        )
        campaign_service.GetKeywordsByAdGroupId(
            AdGroupId=ad_group_ids['long'][0],
            ReturnAdditionalFields=['BiddingScheme']
        )
        
        # Delete the campaign, ad group, keyword, and ad that were previously added. 
        # You should remove this line if you want to view the added entities in the 
        # Bing Ads web application or another tool.

        campaign_service.DeleteCampaigns(
            AccountId=authorization_data.account_id,
            CampaignIds=campaign_ids
        )
        for campaign_id in campaign_ids['long']:
            output_status_message("Deleted CampaignId {0}\n".format(campaign_id))
        
        # This sample will attempt to delete the budget that was created above 
        # if the customer is enabled for shared budgets.
        if enabled_for_shared_budgets:
            campaign_service.DeleteBudgets(
                BudgetIds=budget_ids
            )
            for budget_id in budget_ids['long']:
                output_status_message("Deleted BudgetId {0}\n".format(budget_id))

        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)