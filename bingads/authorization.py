try:
    from urllib.parse import parse_qs, urlparse, quote_plus
except ImportError:
    from urlparse import parse_qs, urlparse
    from urllib import quote_plus
import json

import requests

from .exceptions import OAuthTokenRequestException


class AuthorizationData:
    """ Represents a user who intends to access the corresponding customer and account.

    An instance of this class is required to authenticate with Bing Ads if you are using either
    :class:`.ServiceClient` or :class:`.BulkServiceManager`.
    """

    def __init__(self,
                 account_id=None,
                 customer_id=None,
                 developer_token=None,
                 authentication=None):
        """ Initialize an instance of this class.

        :param account_id: The identifier of the account that owns the entities in the request.
                            Used as the CustomerAccountId header and the AccountId body elements
                            in calls to the Bing Ads web services.
        :type account_id: int
        :param customer_id: The identifier of the customer that owns the account.
                            Used as the CustomerId header element in calls to the Bing Ads web services.
        :type customer_id: int
        :param developer_token: The Bing Ads developer access token.
                            Used as the DeveloperToken header element in calls to the Bing Ads web services.
        :type developer_token: str
        :param authentication: An object representing the authentication method that should be used in calls
                            to the Bing Ads web services.
        :type authentication: Authentication
        """

        self._account_id = account_id
        self._customer_id = customer_id
        self._developer_token = developer_token
        self._authentication = authentication

    @property
    def account_id(self):
        """ The identifier of the account that owns the entities in the request.

        Used as the CustomerAccountId header and the AccountId body elements in calls to the Bing Ads web services.

        :rtype: int
        """

        return self._account_id

    @property
    def customer_id(self):
        """ The identifier of the customer that owns the account.

        Used as the CustomerId header element in calls to the Bing Ads web services.

        :rtype: int
        """

        return self._customer_id

    @property
    def developer_token(self):
        """ The Bing Ads developer access token.

        Used as the DeveloperToken header element in calls to the Bing Ads web services.

        :rtype: str
        """

        return self._developer_token

    @property
    def authentication(self):
        """ An object representing the authentication method that should be used in calls to the Bing Ads web services.

        *See also:*

        * :class:`.OAuthDesktopMobileAuthCodeGrant`
        * :class:`.OAuthDesktopMobileImplicitGrant`
        * :class:`.OAuthWebAuthCodeGrant`
        * :class:`.PasswordAuthentication`

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
    """ The base class for all authentication classes.

    *See also:*

    * :class:`.ServiceClient`
    * :class:`.BulkServiceManager`
    * :class:`.AuthorizationData`
    """

    def enrich_headers(self, headers):
        """ Sets the required header elements for the corresponding Bing Ads service or bulk file upload operation.

        The header elements that the method sets will differ depending on the type of authentication.
        For example if you use one of the OAuth classes, the AuthenticationToken header will be set by this method,
        whereas the UserName and Password headers will remain empty.

        :param headers: Bing Ads service or bulk file upload operation headers.
        :type headers: dict
        :rtype: None
        """

        raise NotImplementedError()


class PasswordAuthentication(Authentication):
    """ Represents a legacy Bing Ads authentication method using user name and password.

    You can use an instance of this class as the authentication property of a :class:`.AuthorizationData` object to
    authenticate with Bing Ads services.
    Existing users with legacy Bing Ads credentials may continue to specify the UserName and Password header elements.
    In future versions of the API, Bing Ads will transition exclusively to Microsoft Account authentication.
    New customers are required to sign up for Bing Ads with a Microsoft Account, and to manage those accounts you must
    use OAuth.
    For example instead of using this :class:`.PasswordAuthentication` class, you would authenticate with an instance
    of either :class:`.OAuthDesktopMobileAuthCodeGrant`, :class:`.OAuthDesktopMobileImplicitGrant`,
    or :class:`.OAuthWebAuthCodeGrant`.
    """

    def __init__(self, user_name, password):
        """ Initializes a new instance of this class using the specified user name and password.

        :param user_name: The Bing Ads user's sign-in user name. You may not set this element to a Microsoft account.
        :type user_name: str
        :param password: The Bing Ads user's sign-in password.
        :type password: str
        """

        self._user_name = user_name
        self._password = password

    @property
    def user_name(self):
        """ The Bing Ads user's sign-in user name. You may not set this element to a Microsoft account.

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
        """ Sets the user name and password as headers elements for Bing Ads service or bulk file upload operation. """

        headers['UserName'] = self.user_name
        headers['Password'] = self.password


class OAuthTokens:
    """ Contains information about OAuth access tokens received from the Microsoft Account authorization service.

    You can get OAuthTokens using the RequestAccessAndRefreshTokens method of RequestAccessAndRefreshTokens method of
    either the :class:`.OAuthDesktopMobileAuthCodeGrant` or :class:`.OAuthWebAuthCodeGrant` classes.
    """

    def __init__(self, access_token=None, access_token_expires_in_seconds=None, refresh_token=None):
        """ Initialize an instance of this class.

        :param access_token: OAuth access token that will be used for authorization in the Bing Ads services.
        :type access_token: (optional) str or None
        :param access_token_expires_in_seconds: (optional) The access token expiration time in seconds.
        :type access_token_expires_in_seconds: int or None
        :param refresh_token: (optional) OAuth refresh token that can be user to refresh an access token.
        :type refresh_token: str or None
        """

        self._access_token = access_token
        self._access_token_expires_in_seconds = access_token_expires_in_seconds
        self._refresh_token = refresh_token

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
    def refresh_token(self):
        """ OAuth refresh token that can be user to refresh an access token.

        :rtype: str
        """

        return self._refresh_token


class OAuthAuthorization(Authentication):
    """ The abstract base class for all OAuth authentication classes.

    You can use this class to dynamically instantiate a derived OAuth authentication class at run time.
    This class cannot be instantiated, and instead you should use either :class:`.OAuthDesktopMobileAuthCodeGrant`,
    :class:`.OAuthDesktopMobileImplicitGrant`, :class:`.OAuthWebAuthCodeGrant`, which extend this class.

    *See also:*

    * :class:`.OAuthDesktopMobileAuthCodeGrant`
    * :class:`.OAuthDesktopMobileImplicitGrant`
    * :class:`.OAuthWebAuthCodeGrant`
    """

    def __init__(self, client_id, oauth_tokens=None):
        """ Initializes a new instance of the OAuthAuthorization class.

        :param client_id: The client identifier corresponding to your registered application.
        :type client_id: str
        :param oauth_tokens: Contains information about OAuth access tokens received from the Microsoft Account authorization service
        :type oauth_tokens: OAuthTokens
        :rtype: str
        """

        if client_id is None:
            raise ValueError('Client id cannot be None.')
        self._client_id = client_id
        self._oauth_tokens = oauth_tokens
        self._state = None

    @property
    def client_id(self):
        """ The client identifier corresponding to your registered application.

        For more information about using a client identifier for authentication, see the
        Client Password Authentication section of the OAuth 2.0 spec at
        http://tools.ietf.org/html/draft-ietf-oauth-v2-15#section-3.1

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

    def enrich_headers(self, headers):
        """ Sets the AuthenticationToken headers elements for Bing Ads service or bulk file upload operation. """

        if self.oauth_tokens is None:
            raise NotImplementedError("OAuth access token hasn't been requested.")
        headers['AuthenticationToken'] = self.oauth_tokens.access_token


class OAuthWithAuthorizationCode(OAuthAuthorization):
    """ Represents a proxy to the Microsoft account authorization service.

    Implement an extension of this class in compliance with the authorization code grant flow for Managing User
    Authentication with OAuth documented at http://go.microsoft.com/fwlink/?LinkID=511609. This is a standard OAuth 2.0
    flow and is defined in detail in the Authorization Code Grant section of the OAuth 2.0 spec at
    http://tools.ietf.org/html/draft-ietf-oauth-v2-15#section-4.1.
    For more information about registering a Bing Ads application, see http://go.microsoft.com/fwlink/?LinkID=511607.
    """

    def __init__(self, client_id, client_secret, redirection_uri, token_refreshed_callback=None, oauth_tokens=None):
        """ Initialize a new instance of this class.

        :param client_id: The client identifier corresponding to your registered application.
        :type client_id: str
        :param client_secret: The client secret corresponding to your registered application, or None if your app is a
        desktop or mobile app.
        :type client_secret: str or None
        :param redirection_uri: The URI to which the user of the app will be redirected after receiving user consent.
        :type redirection_uri: str
        :param token_refreshed_callback: (optional) Call back function when oauth_tokens be refreshed.
        :type token_refreshed_callback: (OAuthTokens)->None or None
        :param oauth_tokens: Contains information about OAuth access tokens received from the Microsoft Account authorization service
        :type oauth_tokens: OAuthTokens
        :return:
        """

        super(OAuthWithAuthorizationCode, self).__init__(client_id, oauth_tokens=oauth_tokens)
        self._client_secret = client_secret
        self._redirection_uri = redirection_uri
        self._token_refreshed_callback = token_refreshed_callback

    def get_authorization_endpoint(self):
        """ Gets the Microsoft Account authorization endpoint where the user should be navigated to give his or her consent.

        :return: The Microsoft Account authorization endpoint.
        :rtype: str
        """
        endpoint = str.format(
            'https://login.live.com/oauth20_authorize.srf?client_id={0}&scope=bingads.manage&response_type={1}&redirect_uri={2}',
            self._client_id,
            'code',
            quote_plus(self._redirection_uri)
        )
        return endpoint if self.state is None else endpoint + '&state=' + self.state

    def request_oauth_tokens_by_response_uri(self, response_uri):
        """ Retrieves OAuth access and refresh tokens from the Microsoft Account authorization service.

        Using the specified authorization response redirection uri.
        For more information, see the Authorization Response section in the OAuth 2.0 spec
        at http://tools.ietf.org/html/draft-ietf-oauth-v2-15#section-4.1.2.

        :param response_uri: The response redirection uri.
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

        self._oauth_tokens = _LiveComOAuthService.get_access_token(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirection_uri,
            grant_type='authorization_code',
            code=code,
        )
        if self.token_refreshed_callback is not None:
            self.token_refreshed_callback(self.oauth_tokens)  # invoke the callback when token refreshed.
        return self.oauth_tokens

    def request_oauth_tokens_by_refresh_token(self, refresh_token):
        """ Retrieves OAuth access and refresh tokens from the Microsoft Account authorization service.

        Using the specified refresh token.
        For more information, see the Refreshing an Access Token section in the OAuth 2.0 spec
        at http://tools.ietf.org/html/draft-ietf-oauth-v2-15#section-6.

        :param refresh_token: The refresh token used to request new access and refresh tokens.
        :type refresh_token: str
        :return: OAuth tokens
        :rtype: OAuthTokens
        """

        self._oauth_tokens = _LiveComOAuthService.get_access_token(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirection_uri,
            grant_type='refresh_token',
            refresh_token=refresh_token,
        )
        if self.token_refreshed_callback is not None:
            self.token_refreshed_callback(self.oauth_tokens)  # invoke the callback when token refreshed.

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
    of an :class:`.AuthorizationData` object to authenticate with Bing Ads services.
    In this case the AuthenticationToken request header will be set to the corresponding OAuthTokens.AccessToken value.

    This class implements the authorization code grant flow for Managing User Authentication with OAuth
    documented at http://go.microsoft.com/fwlink/?LinkID=511609. This is a standard OAuth 2.0 flow and is defined in detail in the
    Authorization Code Grant section of the OAuth 2.0 spec at http://tools.ietf.org/html/draft-ietf-oauth-v2-15#section-4.1.
    For more information about registering a Bing Ads application, see http://go.microsoft.com/fwlink/?LinkID=511607.
    """

    def __init__(self, client_id, oauth_tokens=None):
        """ Initializes a new instance of the this class with the specified client id.

        :param client_id: The client identifier corresponding to your registered application.
        :type client_id: str
        :param oauth_tokens: Contains information about OAuth access tokens received from the Microsoft Account authorization service
        :type oauth_tokens: OAuthTokens
        """

        super(OAuthDesktopMobileAuthCodeGrant, self).__init__(
            client_id,
            None,
            _LiveComOAuthService.DESKTOP_REDIRECTION_URI,
            oauth_tokens=oauth_tokens,
        )


class OAuthWebAuthCodeGrant(OAuthWithAuthorizationCode):
    """ Represents an OAuth authorization object implementing the authorization code grant flow for use in a web application.

    You can use an instance of this class as the AuthorizationData.Authentication property
    of an :class:`.AuthorizationData` object to authenticate with Bing Ads services.
    In this case the AuthenticationToken request header will be set to the corresponding OAuthTokens.AccessToken value.

    This class implements the authorization code grant flow for Managing User Authentication with OAuth
    documented at http://go.microsoft.com/fwlink/?LinkID=511609. This is a standard OAuth 2.0 flow and is defined in detail in the
    Authorization Code Grant section of the OAuth 2.0 spec at http://tools.ietf.org/html/draft-ietf-oauth-v2-15#section-4.1.
    For more information about registering a Bing Ads application, see http://go.microsoft.com/fwlink/?LinkID=511607.
    """

    pass


class OAuthDesktopMobileImplicitGrant(OAuthAuthorization):
    """ Represents an OAuth authorization object implementing the implicit grant flow for use in a desktop or mobile application.

    You can use an instance of this class as the AuthorizationData.Authentication property
    of an :class:`.AuthorizationData` object to authenticate with Bing Ads services.
    In this case the AuthenticationToken request header will be set to the corresponding OAuthTokens.AccessToken value.

    This class implements the implicit grant flow for Managing User Authentication with OAuth
    documented at http://go.microsoft.com/fwlink/?LinkID=511608. This is a standard OAuth 2.0 flow and is defined in detail in the
    Authorization Code Grant section of the OAuth 2.0 spec at http://tools.ietf.org/html/draft-ietf-oauth-v2-15#section-4.1.
    For more information about registering a Bing Ads application, see http://go.microsoft.com/fwlink/?LinkID=511607.
    """

    def __init__(self, client_id, oauth_tokens=None):
        """ Initializes a new instance of the this class with the specified client id.

        :param client_id: The client identifier corresponding to your registered application.
        :type client_id: str
        :param oauth_tokens: Contains information about OAuth access tokens received from the Microsoft Account authorization service
        :type oauth_tokens: OAuthTokens
        """

        super(OAuthDesktopMobileImplicitGrant, self).__init__(client_id, oauth_tokens=oauth_tokens)

    def get_authorization_endpoint(self):
        """ Gets the Microsoft Account authorization endpoint where the user should be navigated to give his or her consent.

        :return: The Microsoft Account authorization endpoint.
        :rtype: str
        """

        endpoint = str.format(
            'https://login.live.com/oauth20_authorize.srf?client_id={0}&scope=bingads.manage&response_type={1}&redirect_uri={2}',
            self.client_id,
            'token',
            _LiveComOAuthService.DESKTOP_REDIRECTION_URI,
        )
        return endpoint if self.state is None else endpoint + '&state=' + self.state

    def extract_access_token_from_uri(self, redirection_uri):
        """ Extracts the access token from the specified redirect URI.

        :param redirection_uri: The redirect URI that contains an access token.
        :type redirection_uri: str
        :return: The :class:`.OAuthTokens` object which contains both the access_token and access_token_expires_in_seconds properties.
        :rtype: OAuthTokens
        """

        parameters = parse_qs(urlparse(redirection_uri).fragment)
        if 'access_token' not in parameters or len(parameters['access_token']) == 0:
            raise ValueError(str.format("Input URI: {0} doesn't contain access_token parameter", redirection_uri))
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
        return _LiveComOAuthService.DESKTOP_REDIRECTION_URI


class _LiveComOAuthService:
    """ Provides method for getting OAuth tokens from the live.com authorization server."""

    def __init__(self):
        pass

    DESKTOP_REDIRECTION_URI = 'https://login.live.com/oauth20_desktop.srf'

    @staticmethod
    def get_access_token(**kwargs):
        """ Calls live.com authorization server with parameters passed in, deserializes the response and returns back OAuth tokens.

        :param kwargs: OAuth parameters for authorization server call.
        :return: OAuth tokens.
        :rtype: OAuthTokens
        """

        if 'client_secret' in kwargs and kwargs['client_secret'] is None:
            del kwargs['client_secret']

        r = requests.post('https://login.live.com/oauth20_token.srf', kwargs, verify=True)
        try:
            r.raise_for_status()
        except Exception:
            error_json = json.loads(r.text)
            raise OAuthTokenRequestException(error_json['error'], error_json['error_description'])

        r_json = json.loads(r.text)
        return OAuthTokens(r_json['access_token'], int(r_json['expires_in']), r_json['refresh_token'])
