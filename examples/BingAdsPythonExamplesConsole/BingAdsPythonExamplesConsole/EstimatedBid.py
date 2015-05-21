from bingads import *

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

    authorization_data=AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    ad_intelligence_service=ServiceClient(
        service='AdIntelligenceService', 
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

        # Set the Currency, Keywords, Language, PublisherCountries, and TargetPositionForAds
        # for the estimated bid by keywords request. 

        currency='USDollar'
        language='English'
        publisher_countries={'string': ['US']}
        match_types={'MatchType': [
            'Broad',
            'Exact',
            'Phrase',
        ]}
        target_position_for_ads='SideBar'

        keyword_and_match_types=ad_intelligence_service.factory.create('ns0:ArrayOfKeywordAndMatchType')
        keyword_and_match_type_1=ad_intelligence_service.factory.create('ns0:KeywordAndMatchType')
        keyword_and_match_type_1.KeywordText='flower'
        keyword_and_match_type_1.MatchTypes=match_types
        #keyword_and_match_types.KeywordAndMatchType.append(keyword_and_match_type_1)
        keyword_and_match_type_2=ad_intelligence_service.factory.create('ns0:KeywordAndMatchType')
        keyword_and_match_type_2.KeywordText='delivery'
        keyword_and_match_type_2.MatchTypes=match_types
        #keyword_and_match_types.KeywordAndMatchType.append(keyword_and_match_type_2)

        keyword_and_match_types={'KeywordAndMatchType': [keyword_and_match_type_1, keyword_and_match_type_2]}

        keyword_estimated_bids=ad_intelligence_service.GetEstimatedBidByKeywords(
            Currency=currency,
            GetBidsAtLevel=0,  # Set GetBidsAtLevel to 0 to get a list of KeywordEstimatedBid.
            Keywords=keyword_and_match_types,
            Language=language,
            PublisherCountries=publisher_countries,
            TargetPositionForAds=target_position_for_ads,
        ).KeywordEstimatedBids

        ad_group_estimated_bid=ad_intelligence_service.GetEstimatedBidByKeywords(
            Currency=currency,
            GetBidsAtLevel=2,  # Set GetBidsAtLevel to 2 to get one ad_group_estimated_bid.
            Keywords=keyword_and_match_types,
            Language=language,
            PublisherCountries=publisher_countries,
            TargetPositionForAds=target_position_for_ads
        ).AdGroupEstimatedBid

        # Print the KeywordEstimatedBids

        if keyword_estimated_bids is not None:
            output_status_message('KeywordEstimatedBids')
            for bid in keyword_estimated_bids['KeywordEstimatedBid']:
                if bid is None:
                    output_status_message('The keyword is not valid.')
                else:
                    output_status_message(bid.Keyword)
                    if len(bid.EstimatedBids) == 0:
                        output_status_message("  There is no bid information available for the keyword.\n")
                    else:
                        for estimated_bid_and_traffic in bid.EstimatedBids['EstimatedBidAndTraffic']:
                            output_status_message("  " + estimated_bid_and_traffic.MatchType);
                            output_status_message("    Estimated Minimum Bid: {0}".format(estimated_bid_and_traffic.EstimatedMinBid))
                            output_status_message("    Average CPC: {0}".format(estimated_bid_and_traffic.AverageCPC))
                            output_status_message(
                                "    Estimated clicks per week: {0} to {1}".format(
                                    estimated_bid_and_traffic.MinClicksPerWeek, 
                                    estimated_bid_and_traffic.MaxClicksPerWeek
                                )
                            )
                            output_status_message(
                                "    Estimated impressions per week: {0} to {1}".format(
                                    estimated_bid_and_traffic.MinImpressionsPerWeek,
                                    estimated_bid_and_traffic.MaxImpressionsPerWeek
                                )
                            )
                            output_status_message(
                                "    Estimated cost per week: {0} to {1}".format(
                                    estimated_bid_and_traffic.MinTotalCostPerWeek, 
                                    estimated_bid_and_traffic.MaxTotalCostPerWeek
                                )
                            )

        output_status_message('AdGroupEstimatedBid')

        output_status_message("  Average CPC: {0}".format(ad_group_estimated_bid.AverageCPC))
        output_status_message("  CTR: {0}".format(ad_group_estimated_bid.CTR))
        output_status_message("  Estimated Ad Group Bid: {0}".format(ad_group_estimated_bid.EstimatedAdGroupBid))
        output_status_message(
            "  Estimated clicks per week: {0} to {1}".format(
                ad_group_estimated_bid.MinClicksPerWeek, 
                ad_group_estimated_bid.MaxClicksPerWeek
            )
        )
        output_status_message(
            "  Estimated impressions per week: {0} to {1}".format(
                ad_group_estimated_bid.MinImpressionsPerWeek,
                ad_group_estimated_bid.MaxImpressionsPerWeek
            )
        )
        output_status_message(
            "  Estimated cost per week: {0} to {1}".format(
                ad_group_estimated_bid.MinTotalCostPerWeek, 
                ad_group_estimated_bid.MaxTotalCostPerWeek
            )
        )

        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

