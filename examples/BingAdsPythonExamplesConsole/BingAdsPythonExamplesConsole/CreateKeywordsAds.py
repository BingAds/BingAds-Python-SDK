from bingads import *

import sys
import webbrowser
from time import gmtime, strftime

# Optionally you can include logging to output traffic, for example the SOAP request and response.
'''
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)
'''

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

def output_ad_results(ads, ad_ids, ad_errors):
    if not hasattr(ad_ids, 'long'):
        return None

    # Since len(ads['Ad']) and len(ad_errors['long']) usually differ, we will need to adjust the ad_errors index 
    # as successful indices are counted. 
    success_count=0 

    # There is an issue in the SUDS library, where if Index 0 of ArrayOfNullableOflong is empty it is not returned. 
    # In this case we will need to adjust the index used to access ad_ids.
    suds_index_0_gap=len(ads['Ad']) - len(ad_ids['long'])

    error_index=0

    for ad_index in range(len(ads['Ad'])):
        attribute_value=None
        if ads['Ad'][ad_index].Type == 'Text':
            attribute_value="Title: {0}".format(ads['Ad'][ad_index].Title)
        elif ads['Ad'][ad_index].Type == 'Mobile':
            attribute_value="Title: {0}".format(ads['Ad'][ad_index].Title)
        elif ads['Ad'][ad_index].Type == 'Product':
            attribute_value="PromotionalText: {0}".format(ads['Ad'][ad_index].PromotionalText)
        else:
            attribute_value="Unknown Ad Type"
        
        if ad_errors \
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
    if not hasattr(keyword_ids, 'long'):
        return None

    # Since len(keywords['Keyword']) and len(keyword_errors['long']) differ, we will need to adjust the keyword_errors index 
    # as successful indices are counted. 
    success_count=0 

    # There is an issue in the SUDS library, where if Index 0 of ArrayOfNullableOflong is empty it is not returned. 
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

        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=campaign_service.factory.create('Campaign')
        campaign.Name='Winter Clothing ' + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description='Winter clothing line.'
        campaign.BudgetType='MonthlyBudgetSpendUntilDepleted'
        campaign.MonthlyBudget=1000
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.DaylightSaving='true' # Accepts 'true', 'false', True, or False
        campaign.Status='Paused'
        campaign.ForwardCompatibilityMap={
            'KeyValuePairOfstringstring': { 
                'key': 'KeywordVariantMatchEnabled', 
                'value': 'false'  # Accepts 'true' or 'false'
            }
        }
        campaigns.Campaign.append(campaign)

        ad_groups=campaign_service.factory.create('ArrayOfAdGroup')
        ad_group=campaign_service.factory.create('AdGroup')
        ad_group.Name="Women's Heated Ski Glove Sale"
        ad_group.AdDistribution='Search'
        ad_group.BiddingModel='Keyword'
        ad_group.PricingModel='Cpc'
        ad_group.Network='OwnedAndOperatedAndSyndicatedSearch'
        ad_group.Status='Paused'
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
        ad_groups.AdGroup.append(ad_group)

        # In this example only the second ad should succeed. The Title of the first ad is empty and not valid,
        # and the third ad is a duplicate of the second ad. 
        
        ads=campaign_service.factory.create('ArrayOfAd')
        
        for index in range(3):
            text_ad=campaign_service.factory.create('TextAd')
            text_ad.DestinationUrl='http://www.alpineskihouse.com/winterglovesale'
            text_ad.DisplayUrl='AlipineSkiHouse.com'
            text_ad.Text='Huge Savings on heated gloves.'
            text_ad.Title='Winter Glove Sale'
            text_ad.Type='Text'
            text_ad.Status=None
            text_ad.EditorialStatus=None
            ads.Ad.append(text_ad)
        
        ads.Ad[0].Title=''

        # In this example only the second keyword should succeed. The Text of the first keyword exceeds the limit,
        # and the third keyword is a duplicate of the second keyword.  

        keywords=campaign_service.factory.create('ArrayOfKeyword')
        
        for index in range(3):
            keyword=campaign_service.factory.create('Keyword')
            keyword.Bid.Amount=0.47
            keyword.Param2='10% Off'
            keyword.MatchType='Broad'
            keyword.Text='Brand-A Gloves'
            keyword.Status=None
            keyword.EditorialStatus=None
            keywords.Keyword.append(keyword)
        
        keywords.Keyword[0].Text=(
            "Brand-A Gloves Brand-A Gloves Brand-A Gloves Brand-A Gloves Brand-A Gloves "
		    "Brand-A Gloves Brand-A Gloves Brand-A Gloves Brand-A Gloves Brand-A Gloves "
		    "Brand-A Gloves Brand-A Gloves Brand-A Gloves Brand-A Gloves Brand-A Gloves"
        )

        # Add the campaign, ad group, keywords, and ads

        campaign_ids=campaign_service.AddCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=campaigns
        )['long']

        output_campaign_ids(campaign_ids)

        ad_group_ids=campaign_service.AddAdGroups(
            CampaignId=campaign_ids[0],
            AdGroups=ad_groups
        )['long']
        output_ad_group_ids(ad_group_ids)

        add_ads_response=campaign_service.AddAds(
            AdGroupId=ad_group_ids[0],
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
            AdGroupId=ad_group_ids[0],
            Keywords=keywords
        )
        keyword_ids={
                'long': add_keywords_response.KeywordIds['long'] if add_keywords_response.KeywordIds else None
            }
        keyword_errors={
                'BatchError': add_keywords_response.PartialErrors['BatchError'] if add_keywords_response.PartialErrors else None
            } 
    
        output_keyword_results(keywords, keyword_ids, keyword_errors)

        # Delete the campaign, ad group, keyword, and ad that were previously added. 
        # You should remove this line if you want to view the added entities in the 
        # Bing Ads web application or another tool.
        campaign_service.DeleteCampaigns(
            AccountId=authorization_data.account_id,
            CampaignIds={
                    'long': campaign_ids
                }
        )

        for campaign_id in campaign_ids:
            output_status_message("Deleted CampaignId {0}\n".format(campaign_id))

        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

