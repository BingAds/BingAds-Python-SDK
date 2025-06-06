import sys
import webbrowser
from time import gmtime, strftime
from typing import Optional, List, Dict

from openapi_client.models.campaign import *
from openapi_client.models.customer import *
from bingads.authorization import *
from bingads.service_client import ServiceClient

# Required
DEVELOPER_TOKEN = 'BBD37VB98'  # Universal token for sandbox
ENVIRONMENT = 'sandbox'  # If you use 'production' then you must also update the DEVELOPER_TOKEN value.

# The CLIENT_ID is required and CLIENT_STATE is recommended.
# The REFRESH_TOKEN should always be in a secure location.
CLIENT_ID = '2663d04e-2635-47aa-b8e6-3682588841a2'
CLIENT_STATE = 'ClientStateGoesHere'
REFRESH_TOKEN = "refresh.txt"

# Constants for campaign and criterion types
ALL_CAMPAIGN_TYPES=['Audience Search Shopping']
ALL_TARGET_CAMPAIGN_CRITERION_TYPES=['Age DayTime Device Gender Location LocationIntent Radius']
ALL_TARGET_AD_GROUP_CRITERION_TYPES=['Age DayTime Device Gender Location LocationIntent Radius']

ALL_AD_TYPES={
    'AdType': ['AppInstall', 'DynamicSearch', 'ExpandedText', 'Product', 'ResponsiveAd', 'ResponsiveSearchAd', 'Text']
}


def authenticate(authorization_data):
    """
    Authenticate the user and set up account details.
    """
    # Authenticate with OAuth
    authenticate_with_oauth(authorization_data)

    # Create customer management service client

    customer_service = ServiceClient(
        'CustomerManagementService',
        13,
        authorization_data=authorization_data,
        environment=ENVIRONMENT
    )

    get_user_request = GetUserRequest(UserId=None)

    # Get the current authenticated Bing Ads user
    user = customer_service.GetUser(get_user_request).User
    accounts = search_accounts_by_user_id(customer_service, user.Id)

    # For this example we'll use the first account
    authorization_data.account_id = accounts[0].Id
    authorization_data.customer_id = accounts[0].ParentCustomerId


def authenticate_with_oauth(authorization_data):
    authentication = OAuthDesktopMobileAuthCodeGrant(
        client_id=CLIENT_ID,
        env=ENVIRONMENT
    )

    # It is recommended that you specify a non guessable 'state' request parameter to help prevent
    # cross site request forgery (CSRF).
    authentication.state = CLIENT_STATE

    # Assign this authentication instance to the authorization_data.
    authorization_data.authentication = authentication

    # Register the callback function to automatically save the refresh token anytime it is refreshed.
    # Uncomment this line if you want to store your refresh token. Be sure to save your refresh token securely.
    authorization_data.authentication.token_refreshed_callback = save_refresh_token

    refresh_token = get_refresh_token()

    try:
        # If we have a refresh token let's refresh it
        if refresh_token is not None:
            authorization_data.authentication.request_oauth_tokens_by_refresh_token(refresh_token)
        else:
            request_user_consent(authorization_data)
    except OAuthTokenRequestException:
        # The user could not be authenticated or the grant is expired.
        # The user must first sign in and if needed grant the client application access to the requested scope.
        request_user_consent(authorization_data)


def request_user_consent(authorization_data):
    webbrowser.open(authorization_data.authentication.get_authorization_endpoint(), new=1)
    # For Python 3.x use 'input' instead of 'raw_input'
    if (sys.version_info.major >= 3):
        response_uri = input(
            "You need to provide consent for the application to access your Bing Ads accounts. " \
            "After you have granted consent in the web browser for the application to access your Bing Ads accounts, " \
            "please enter the response URI that includes the authorization 'code' parameter: \n"
        )
    else:
        response_uri = raw_input(
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
    file = None
    try:
        file = open(REFRESH_TOKEN)
        line = file.readline()
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
    with open(REFRESH_TOKEN, "w+") as file:
        file.write(oauth_tokens.refresh_token)
        file.close()
    return None


def search_accounts_by_user_id(customer_service, user_id: int) -> List[Dict]:
    """
    Search for accounts accessible by the user.
    
    Args:
        customer_service: The customer management service client
        user_id: The user ID to search accounts for
        
    Returns:
        List of advertiser accounts
    """
    predicate = Predicate(
        field="UserId",
        operator=PredicateOperator.EQUALS,
        value=str(user_id)
    )

    accounts = []
    page_index = 0
    page_size = 100
    
    while True:
        paging = Paging(
            index=page_index,
            size=page_size
        )
        
        request = SearchAccountsRequest(
            page_info=paging,
            predicates=[predicate]
        )
        
        response: SearchAccountsResponse = customer_service.search_accounts(request)
        
        if not response.accounts:
            break
            
        accounts.extend(response.accounts)
        
        if len(response.accounts) < page_size:
            break
            
        page_index += 1

    return accounts
