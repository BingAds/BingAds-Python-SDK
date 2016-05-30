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

        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=campaign_service.factory.create('Campaign')
        campaign.Name="Summer Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description="Summer shoes line."
        campaign.BudgetType='MonthlyBudgetSpendUntilDepleted'
        campaign.MonthlyBudget=1000
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.DaylightSaving='true' # Accepts 'true', 'false', True, or False
        campaign.Status='Paused'
        campaigns.Campaign.append(campaign)

        ad_groups=campaign_service.factory.create('ArrayOfAdGroup')
        ad_group=campaign_service.factory.create('AdGroup')
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

        #You could use a tracking template which would override the campaign level
        #tracking template. Tracking templates defined for lower level entities 
        #override those set for higher level entities.
        #In this example we are using the campaign level tracking template.
        ad_group.TrackingUrlTemplate=None

        ad_groups.AdGroup.append(ad_group)

        # In this example only the first 3 ads should succeed. 
        # The Title of the fourth ad is empty and not valid,
        # and the fifth ad is a duplicate of the second ad.
        
        ads=campaign_service.factory.create('ArrayOfAd')
        
        for index in range(5):
            text_ad=campaign_service.factory.create('TextAd')
            text_ad.Title='Red Shoe Sale'
            text_ad.Text='Huge Savings on red shoes.'
            text_ad.DisplayUrl='Contoso.com'
            text_ad.Type='Text'
            text_ad.Status=None
            text_ad.EditorialStatus=None

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
            keyword=campaign_service.factory.create('Keyword')
            keyword.Bid.Amount=0.47
            keyword.Param2='10% Off'
            keyword.MatchType='Broad'
            keyword.Text='Brand-A Shoes'
            keyword.Status=None
            keyword.EditorialStatus=None
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
        update_campaigns=campaign_service.factory.create('ArrayOfCampaign')
        update_campaign=campaign_service.factory.create('Campaign')
        update_campaign.BudgetType=None
        update_campaign.Id=campaign_ids['long'][0]
        update_campaign.MonthlyBudget=500
        update_campaign.Status=None
        update_campaigns.Campaign.append(update_campaign)

        # As an exercise you can step through using the debugger and view the results.
        campaign_service.GetCampaignsByIds(
            AccountId=authorization_data.account_id,
            CampaignIds=campaign_ids,
            CampaignType=['SearchAndContent Shopping']
        )
        campaign_service.UpdateCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=update_campaigns
        )
        campaign_service.GetCampaignsByIds(
            AccountId=authorization_data.account_id,
            CampaignIds=campaign_ids,
            CampaignType=['SearchAndContent Shopping']
        )


        # Update the Text for the 3 successfully created ads, and update some UrlCustomParameters.
        update_ads=campaign_service.factory.create('ArrayOfAd')

        # Set the  element to null or empty to retain any 
        # existing custom parameters.
        text_ad_0=campaign_service.factory.create('TextAd')
        text_ad_0.Id=ad_ids['long'][0]
        text_ad_0.Text='Huge Savings on All Red Shoes.'
        text_ad_0.UrlCustomParameters=None
        text_ad_0.Type='Text'
        text_ad_0.Status=None
        text_ad_0.EditorialStatus=None
        update_ads.Ad.append(text_ad_0)

        # To remove all custom parameters, set the Parameters element of the 
        # CustomParameters object to null or empty.
        text_ad_1=campaign_service.factory.create('TextAd')
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
        text_ad_1.Status=None
        text_ad_1.EditorialStatus=None
        update_ads.Ad.append(text_ad_1)

        # To remove a subset of custom parameters, specify the custom parameters that 
        # you want to keep in the Parameters element of the CustomParameters object.
        text_ad_2=campaign_service.factory.create('TextAd')
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
        text_ad_2.Status=None
        text_ad_2.EditorialStatus=None
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
        update_keyword=campaign_service.factory.create('Keyword')
        update_keyword.Id=keyword_ids['long'][0]
        update_keyword.MatchType=None
        update_keyword.Status=None
        update_keyword.EditorialStatus=None

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
        )
        campaign_service.UpdateKeywords(
            AdGroupId=ad_group_ids['long'][0],
            Keywords=update_keywords
        )
        campaign_service.GetKeywordsByAdGroupId(
            AdGroupId=ad_group_ids['long'][0],
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

        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

