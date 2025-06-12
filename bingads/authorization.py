from urllib.parse import parse_qs, urlparse, quote_plus
import json
from datetime import datetime, timedelta
import requests
from openapi_client.exceptions import ApiException

PRODUCTION = 'production'
SANDBOX = 'sandbox'
MSADS_MANAGE = 'msads.manage'
ADS_MANAGE = 'ads.manage'
BINGADS_MANAGE = 'bingads.manage'
MSA_PROD = 'msa.prod'


class OAuthTokenRequestException(ApiException):
    """OAuth token request exception that includes error details from the OAuth service."""

    def __init__(self, error_code, error_description):
        super(OAuthTokenRequestException, self).__init__(
            status=None,
            reason=f"OAuth token request failed. Error: {error_code}. Description: {error_description}"
        )
        self.error_code = error_code
        self.error_description = error_description


class AuthorizationData:
    """ Represents a user who intends to access the corresponding customer and account.

    An instance of this class is required to authenticate with Bing Ads REST API services.
    """

    def __init__(self,
                 account_id=None,
                 customer_id=None,
                 developer_token=None,
                 authentication=None):
        """ Initialize an instance of this class.

        :param account_id: The identifier of the account that owns the entities in the request.
        :type account_id: int
        :param customer_id: The identifier of the customer that owns the account.
        :type customer_id: int
        :param developer_token: The Bing Ads developer access token.
        :type developer_token: str
        :param authentication: An object representing the authentication method.
        :type authentication: Authentication
        """

        self._account_id = account_id
        self._customer_id = customer_id
        self._developer_token = developer_token
        self._authentication = authentication

    @property
    def account_id(self):
        """ The identifier of the account that owns the entities in the request.
        :rtype: int
        """
        return self._account_id

    @property
    def customer_id(self):
        """ The identifier of the customer that owns the account.
        :rtype: int
        """
        return self._customer_id

    @property
    def developer_token(self):
        """ The Bing Ads developer access token.
        :rtype: str
        """
        return self._developer_token

    @property
    def authentication(self):
        """ An object representing the authentication method.
        :rtype: Authentication
        """
        return self._authentication

    @account_id.setter
    def account_id(self, account_id):
        self._account_id = account_id

    @customer_id.setter
    def customer_id(self, customer_id):
        self._customer_id = customer_id

    @developer_token.setter
    def developer_token(self, developer_token):
        self._developer_token = developer_token

    @authentication.setter
    def authentication(self, authentication):
        self._authentication = authentication


class Authentication(object):
    """ The base class for all authentication classes. """

    def enrich_headers(self, headers):
        """ Gets the required header elements for the corresponding REST API call.

        :return: Dictionary containing authentication headers
        :rtype: dict
        """
        raise NotImplementedError()


class PasswordAuthentication(Authentication):
    """ Represents a legacy authentication method using user name and password. """

    def __init__(self, user_name, password):
        """ Initialize an instance of this class.

        :param user_name: The Bing Ads user's sign-in user name.
        :type user_name: str
        :param password: The Bing Ads user's sign-in password.
        :type password: str
        """
        self._user_name = user_name
        self._password = password

    @property
    def user_name(self):
        """ The Bing Ads user's sign-in user name.
        :rtype: str
        """
        return self._user_name

    @property
    def password(self):
        """ The Bing Ads user's sign-in password.
        :rtype: str
        """
        return self._password

    def enrich_headers(self, headers):
        """ Gets the username/password authentication headers.
        :return: Dictionary containing authentication headers
        :rtype: dict
        """
        auth_headers = {
            'UserName': self.user_name,
            'Password': self.password
        }
        headers.update(auth_headers)


class OAuthTokens:
    """ Contains information about OAuth access tokens received from the Microsoft Account authorization service. """

    def __init__(self, access_token=None, access_token_expires_in_seconds=None, refresh_token=None, response_json = None):
        """ Initialize an instance of this class.

        :param access_token: OAuth access token for authorization
        :type access_token: str
        :param access_token_expires_in_seconds: The access token expiration time in seconds
        :type access_token_expires_in_seconds: int
        :param refresh_token: OAuth refresh token that can be used to refresh an access token
        :type refresh_token: str
        """
        self._access_token = access_token
        self._access_token_expires_in_seconds = access_token_expires_in_seconds
        self._refresh_token = refresh_token
        self._response_json = response_json
        self._access_token_received_datetime = datetime.utcnow()

    @property
    def access_token_received_datetime(self):
        """ The datetime when access token was received

        :rtype: datetime
        """
        return self._access_token_received_datetime

    @property
    def access_token(self):
        """ OAuth access token that will be used for authorization in the Bing Ads services.

        :rtype: str
        """
        return self._access_token

    @property
    def access_token_expires_in_seconds(self):
        """ Expiration time for the corresponding access token in seconds.

        :rtype: int
        """
        return self._access_token_expires_in_seconds

    @property
    def access_token_expired(self):
        """ Whether the access token has been expired.

        :rtype: bool
        """
        return self.access_token_expires_in_seconds is not None and \
            self.access_token_expires_in_seconds > 0 and \
            datetime.utcnow() > self.access_token_received_datetime + timedelta(
                seconds=self.access_token_expires_in_seconds)

    @property
    def refresh_token(self):
        """ OAuth refresh token that can be user to refresh an access token.

        :rtype: str
        """
        return self._refresh_token

    @property
    def response_json(self):
        """ OAuth whole attribute that got along with access token.

        :rtype: dictionary
        """
        return self._response_json


class OAuthAuthorization(Authentication):
    """ The abstract base class for all OAuth authentication classes.

    You can use this class to dynamically instantiate a derived OAuth authentication class at run time.
    This class cannot be instantiated, and instead you should use either :class:`.OAuthDesktopMobileAuthCodeGrant`,
    :class:`.OAuthDesktopMobileImplicitGrant`, :class:`.OAuthWebAuthCodeGrant`, which extend this class.
    """

    def __init__(self, client_id, oauth_tokens=None, env=PRODUCTION, oauth_scope=MSADS_MANAGE, tenant='common',
                 use_msa_prod=True):
        """ Initialize an instance of this class.

        :param client_id: The client identifier corresponding to your registered application.
        :type client_id: str
        :param oauth_tokens: OAuth token information
        :type oauth_tokens: OAuthTokens
        """
        if client_id is None:
            raise ValueError('Client id cannot be None.')
        self._client_id = client_id
        self._oauth_tokens = oauth_tokens
        self._state = None
        self.environment = env
        self._oauth_scope = MSA_PROD if env == SANDBOX and use_msa_prod else oauth_scope
        self._tenant = tenant

    def enrich_headers(self, headers):
        """ Gets the OAuth Bearer token authentication headers.
        :return: Dictionary containing authentication headers
        :rtype: dict
        """
        if self.oauth_tokens is None or self.oauth_tokens.access_token is None:
            raise ValueError("OAuth access token hasn't been requested.")
        auth_headers =  {
            'Authorization': 'Bearer ' + self.oauth_tokens.access_token
        }
        headers.update(auth_headers)

    @property
    def tenant(self):
        """ tenant
        :rtype: str
        """
        return self._tenant

    @property
    def client_id(self):
        """ The client identifier corresponding to your registered application.

        For more information about using a client identifier for authentication, see the
        Client Password Authentication section of the OAuth 2.0 spec at
        https://tools.ietf.org/html/rfc6749#section-4.1

        :rtype: str
        """
        return self._client_id

    @property
    def oauth_tokens(self):
        """ Contains information about OAuth access tokens received from the Microsoft Account authorization service.

        :rtype: OAuthTokens
        """
        return self._oauth_tokens

    @property
    def state(self):
        """ An opaque value used by the client to maintain state between the request and callback
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, value):
        """ An opaque value used by the client to maintain state between the request and callback
        :rtype: str
        """
        self._state = value

    @property
    def redirection_uri(self):
        """ The URI to which the user of the app will be redirected after receiving user consent.

        :rtype: str
        """
        raise NotImplementedError()

    def get_authorization_endpoint(self):
        """ Gets the Microsoft Account authorization endpoint where the user should be navigated to give his or her consent.

        :return: The Microsoft Account authorization endpoint.
        :rtype: str
        """
        raise NotImplementedError()


class OAuthWithAuthorizationCode(OAuthAuthorization):
    """ Represents a proxy to the Microsoft account authorization service.

    Implementation of the authorization code grant flow for Managing User Authentication with OAuth.
    This is a standard OAuth 2.0 flow defined in the Authorization Code Grant section of the OAuth 2.0 spec
    at https://tools.ietf.org/html/rfc6749#section-4.1.
    """

    def __init__(self, client_id, client_secret, redirection_uri, token_refreshed_callback=None,
                 oauth_tokens=None, env=PRODUCTION, oauth_scope=MSADS_MANAGE, tenant="common", use_msa_prod=True):
        """ Initialize an instance of this class.

        :param client_id: The client identifier corresponding to your registered application.
        :type client_id: str
        :param client_secret: The client secret for your registered application.
        :type client_secret: str
        :param redirection_uri: The URI to which your client browser will be redirected after receiving user consent.
        :type redirection_uri: str
        :param token_refreshed_callback: Optional callback function when oauth_tokens are refreshed.
        :type token_refreshed_callback: OAuthTokens->None or None
        """
        super(OAuthWithAuthorizationCode, self).__init__(
            client_id=client_id,
            oauth_tokens=oauth_tokens,
            env=env,
            oauth_scope=oauth_scope,
            tenant=tenant,
            use_msa_prod=use_msa_prod
        )
        self._client_secret = client_secret
        self._redirection_uri = redirection_uri
        self._token_refreshed_callback = token_refreshed_callback

    def get_authorization_endpoint(self):
        """ Gets the Microsoft Account authorization endpoint where the user should be navigated to give consent.

        :return: The Microsoft Account authorization endpoint.
        :rtype: str
        """
        endpoint_url = _UriOAuthService.AUTHORIZE_URI[(self.environment, self._oauth_scope)]
        if self.environment == PRODUCTION and (self._oauth_scope == MSADS_MANAGE or self._oauth_scope == ADS_MANAGE):
            endpoint_url = endpoint_url.replace('common', self.tenant)

        endpoint = str.format(
            endpoint_url,
            self._client_id,
            'code',
            quote_plus(self._redirection_uri)
        )

        return endpoint if self.state is None else endpoint + '&state=' + self.state

    def request_oauth_tokens_by_response_uri(self, response_uri, **kwargs):
        """ Request OAuth tokens using the authorization response URI.

        :param response_uri: The response redirection URI.
        :type response_uri: str
        :return: OAuth tokens
        :rtype: OAuthTokens
        """
        parameters = parse_qs(urlparse(response_uri).query)
        if 'code' not in parameters or len(parameters['code']) == 0:
            raise ValueError(
                "Uri passed doesn't contain code param. "
                "Please make sure the uri has a code in it, for example http://myurl.com?code=123"
            )
        code = parameters['code'][0]

        self._oauth_tokens = _UriOAuthService.get_access_token(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirection_uri,
            grant_type='authorization_code',
            environment=self.environment,
            code=code,
            oauth_scope=self._oauth_scope,
            tenant=self.tenant,
            **kwargs
        )
        if self.token_refreshed_callback is not None:
            self.token_refreshed_callback(self.oauth_tokens)
        return self.oauth_tokens

    def request_oauth_tokens_by_refresh_token(self, refresh_token):
        """ Request new OAuth tokens using a refresh token.

        :param refresh_token: The refresh token used to request new tokens.
        :type refresh_token: str
        :return: OAuth tokens
        :rtype: OAuthTokens
        """
        self._oauth_tokens = _UriOAuthService.get_access_token(
            client_id=self.client_id,
            client_secret=self.client_secret,
            grant_type='refresh_token',
            refresh_token=refresh_token,
            environment=self.environment,
            scope=_UriOAuthService.SCOPE[(self.environment, self._oauth_scope)],
            oauth_scope=self._oauth_scope,
            tenant=self.tenant
        )
        if self.token_refreshed_callback is not None:
            self.token_refreshed_callback(self.oauth_tokens)
        return self.oauth_tokens

    @property
    def client_secret(self):
        """ The client secret corresponding to your registered application, or None if your app is a desktop or mobile app.

        :rtype: str
        """

        return self._client_secret

    @property
    def redirection_uri(self):
        """ The URI to which your client browser will be redirected after receiving user consent.

        :rtype: str
        """

        return self._redirection_uri

    @property
    def token_refreshed_callback(self):
        """ The callback function registered, will be invoked after oauth tokens has been refreshed.

        :rtype: OAuthTokens->None
        """

        return self._token_refreshed_callback

    @client_secret.setter
    def client_secret(self, client_secret):
        self._client_secret = client_secret

    @redirection_uri.setter
    def redirection_uri(self, redirection_uri):
        self._redirection_uri = redirection_uri

    @token_refreshed_callback.setter
    def token_refreshed_callback(self, token_refreshed_callback):
        self._token_refreshed_callback = token_refreshed_callback


class OAuthDesktopMobileAuthCodeGrant(OAuthWithAuthorizationCode):
    """ Represents an OAuth authorization object implementing the authorization code grant flow for use in a desktop
    or mobile application.

    You can use an instance of this class as the AuthorizationData.Authentication property
    to authenticate with Bing Ads REST API services.
    """

    def __init__(self, client_id, oauth_tokens=None, env=PRODUCTION, oauth_scope=MSADS_MANAGE, tenant='common', use_msa_prod=True):
        """ Initializes a new instance of this class with the specified client id.

        :param client_id: The client identifier corresponding to your registered application.
        :type client_id: str
        :param oauth_tokens: OAuth token information
        :type oauth_tokens: OAuthTokens
        """
        effective_scope = MSA_PROD if env == SANDBOX and use_msa_prod else oauth_scope
        super(OAuthDesktopMobileAuthCodeGrant, self).__init__(
            client_id,
            None,  # client secret not needed for desktop/mobile apps
            _UriOAuthService.REDIRECTION_URI[(env, effective_scope)],
            oauth_tokens=oauth_tokens,
            env=env,
            oauth_scope=effective_scope,
            tenant=tenant,
            use_msa_prod=use_msa_prod
        )


class OAuthWebAuthCodeGrant(OAuthWithAuthorizationCode):
    """ Represents an OAuth authorization object implementing the authorization code grant flow for use in a web application.

    You can use an instance of this class as the AuthorizationData.Authentication property
    to authenticate with Bing Ads REST API services.
    """
    pass


class OAuthDesktopMobileImplicitGrant(OAuthAuthorization):
    """ Represents an OAuth authorization object implementing the implicit grant flow for use in a desktop or mobile application.

    You can use an instance of this class as the AuthorizationData.Authentication property
    to authenticate with Bing Ads REST API services.
    """

    def __init__(self, client_id, oauth_tokens=None, env=PRODUCTION, oauth_scope=MSADS_MANAGE, tenant='common',
                 use_msa_prod=True):
        """ Initialize an instance of this class.

        :param client_id: The client identifier corresponding to your registered application.
        :type client_id: str
        :param oauth_tokens: OAuth token information
        :type oauth_tokens: OAuthTokens
        """
        effective_scope = MSA_PROD if env == SANDBOX and use_msa_prod else oauth_scope
        super(OAuthDesktopMobileImplicitGrant, self).__init__(client_id, oauth_tokens=oauth_tokens, env=env,
                                                              oauth_scope=effective_scope, tenant=tenant)

    def get_authorization_endpoint(self):
        """ Gets the Microsoft Account authorization endpoint for implicit grant flow.

        :return: The Microsoft Account authorization endpoint.
        :rtype: str
        """
        endpoint_url = _UriOAuthService.AUTHORIZE_URI[(self.environment, self._oauth_scope)]
        if self.environment == PRODUCTION and (self._oauth_scope == MSADS_MANAGE or self._oauth_scope == ADS_MANAGE):
            endpoint_url = endpoint_url.replace('common', self.tenant)

        endpoint = str.format(
            endpoint_url,
            self.client_id,
            'token',
            _UriOAuthService.REDIRECTION_URI[(self.environment, self._oauth_scope)],
        )

        return endpoint if self.state is None else endpoint + '&state=' + self.state

    def extract_access_token_from_uri(self, redirection_uri):
        """ Extract the access token from the specified redirect URI.

        :param redirection_uri: The redirect URI that contains an access token
        :type redirection_uri: str
        :return: OAuth tokens
        :rtype: OAuthTokens
        """
        parameters = parse_qs(urlparse(redirection_uri).fragment)
        if 'access_token' not in parameters or len(parameters['access_token']) == 0:
            raise ValueError(f"Input URI: {redirection_uri} doesn't contain access_token parameter")
        access_token = parameters['access_token'][0]
        if 'expires_in' not in parameters or len(parameters['expires_in']) == 0:
            expires_in = None
        else:
            expires_in = parameters['expires_in'][0]
        self._oauth_tokens = OAuthTokens(
            access_token,
            int(expires_in) if expires_in is not None else None
        )
        return self.oauth_tokens

    @property
    def redirection_uri(self):
        return _UriOAuthService.REDIRECTION_URI[(self.environment, self._oauth_scope)]


class _UriOAuthService:
    """ Provides method for getting OAuth tokens from the live.com authorization server."""

    def __init__(self):
        pass

    REDIRECTION_URI={
        (PRODUCTION, MSADS_MANAGE):   'https://login.microsoftonline.com/common/oauth2/nativeclient',
        (PRODUCTION, ADS_MANAGE):     'https://login.microsoftonline.com/common/oauth2/nativeclient',
        (PRODUCTION, BINGADS_MANAGE): 'https://login.live.com/oauth20_desktop.srf',
        (SANDBOX, MSADS_MANAGE):      'https://login.windows-ppe.net/common/oauth2/nativeclient',
        (SANDBOX, MSA_PROD):          'https://login.microsoftonline.com/common/oauth2/nativeclient'
    }
    AUTH_TOKEN_URI={
        (PRODUCTION, MSADS_MANAGE):   'https://login.microsoftonline.com/common/oauth2/v2.0/token',
        (PRODUCTION, ADS_MANAGE):     'https://login.microsoftonline.com/common/oauth2/v2.0/token',
        (PRODUCTION, BINGADS_MANAGE): 'https://login.live.com/oauth20_token.srf',
        (SANDBOX, MSADS_MANAGE):      'https://login.windows-ppe.net/consumers/oauth2/v2.0/token',
        (SANDBOX, MSA_PROD):          'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    }
    AUTHORIZE_URI={
        (PRODUCTION, MSADS_MANAGE):   'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={0}&scope=https%3A%2F%2Fads.microsoft.com%2Fmsads.manage%20offline_access&response_type={1}&redirect_uri={2}',
        (PRODUCTION, ADS_MANAGE):     'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={0}&scope=https%3A%2F%2Fads.microsoft.com%2Fads.manage%20offline_access&response_type={1}&redirect_uri={2}',
        (PRODUCTION, BINGADS_MANAGE): 'https://login.live.com/oauth20_authorize.srf?client_id={0}&scope=bingads.manage&response_type={1}&redirect_uri={2}',
        (SANDBOX, MSADS_MANAGE):      'https://login.windows-ppe.net/consumers/oauth2/v2.0/authorize?client_id={0}&scope=https://api.ads.microsoft.com/msads.manage%20offline_access&response_type={1}&redirect_uri={2}&prompt=login',
        (SANDBOX, MSA_PROD):          'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={0}&scope=https%3A%2F%2Fsi.ads.microsoft.com%2Fmsads.manage%20offline_access&response_type={1}&redirect_uri={2}'
    }
    SCOPE={
        (PRODUCTION, MSADS_MANAGE):   'https://ads.microsoft.com/msads.manage offline_access',
        (PRODUCTION, ADS_MANAGE):     'https://ads.microsoft.com/ads.manage offline_access',
        (PRODUCTION, BINGADS_MANAGE): 'bingads.manage',
        (SANDBOX, MSADS_MANAGE):      'https://api.ads.microsoft.com/msads.manage offline_access',
        (SANDBOX, MSA_PROD):          'https://si.ads.microsoft.com/msads.manage offline_access'
    }

    @staticmethod
    def get_access_token(**kwargs):

        """ Calls live.com authorization server with parameters passed in, deserializes the response and returns back OAuth tokens.

        :param kwargs: OAuth parameters for authorization server call.
        :return: OAuth tokens.
        :rtype: OAuthTokens
        """

        if 'client_secret' in kwargs and kwargs['client_secret'] is None:
            del kwargs['client_secret']

        if 'oauth_scope' in kwargs and kwargs['oauth_scope'] == 'bingads.manage':
            del kwargs['tenant']

        auth_token_url = _UriOAuthService.AUTH_TOKEN_URI[(kwargs['environment'], kwargs['oauth_scope'])]

        if 'tenant' in kwargs and kwargs['tenant'] is not None:
            auth_token_url = auth_token_url.replace('common', kwargs['tenant'])

        # default timeout set to 300 secs
        r = requests.post(auth_token_url, kwargs, verify=True, timeout=300)
        try:
            r.raise_for_status()
        except Exception:
            error_json = json.loads(r.text)
            raise OAuthTokenRequestException(error_json.get('error'), error_json.get('error_description'))

        r_json = json.loads(r.text)
        return OAuthTokens(r_json['access_token'], int(r_json['expires_in']), r_json['refresh_token'], r_json)
