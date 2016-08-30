from suds.client import Client, Factory, WebFault, ObjectCache  # noqa

from .authorization import *
from .service_info import SERVICE_INFO_DICT, SERVICE_INFO_DICT_V10
from .manifest import USER_AGENT
from getpass import getuser
from tempfile import gettempdir
from os import path


class ServiceClient:
    """ Provides an interface for calling the methods of the specified Bing Ads service."""

    def __init__(self, service, authorization_data=None, environment='production', version='v10', **suds_options):
        """ Initializes a new instance of this class.

        :param service: The service name.
        :type service: str
        :param authorization_data: (optional) The authorization data, if not provided, cannot call operations on service
        :type authorization_data: AuthorizationData or None
        :param environment: (optional) The environment name, can only be 'production' or 'sandbox', the default is 'production'
        :type environment: str
        :param version: to specify the service version, only support v9 and v10, valid input is: 9, 10, 'v9', 'v10', the default is 'v10'
        :param suds_options: The suds options need to pass to suds client
        """

        self._input_service = service
        self._input_environment = environment
        self._authorization_data = authorization_data
        self._refresh_oauth_tokens_automatically = True
        self._version = ServiceClient._format_version(version)

        # TODO This is a temp fix for set default suds temp folder with user info, suds development branch has already fixed it.
        if 'cache' not in suds_options:
            location = path.join(gettempdir(), 'suds', getuser())
            suds_options['cache'] = ObjectCache(location, days=1)
        # set cachingpolicy to 1 to reuse WSDL cache files, otherwise will only reuse XML files
        if 'cachingpolicy' not in suds_options:
            suds_options['cachingpolicy'] = 1
        self._options = suds_options

        self._service = ServiceClient._format_service(service)
        self._environment = ServiceClient._format_environment(environment)

        self._soap_client = Client(self.service_url, **suds_options)

    def __getattr__(self, name):
        # Set authorization data and options before every service call.

        self.set_options(**self._options)
        return _ServiceCall(self, name)

    def set_options(self, **kwargs):
        """ Set suds options, these options will be passed to suds.

        :param kwargs: suds options.
        :rtype: None
        """

        self._options = kwargs
        kwargs = ServiceClient._ensemble_header(self.authorization_data, **self._options)
        self._soap_client.set_options(**kwargs)

    @property
    def authorization_data(self):
        """ Represents a user who intends to access the corresponding customer and account.

        :rtype: AuthorizationData
        """

        return self._authorization_data

    @property
    def soap_client(self):
        """ The internal suds soap client.

        :rtype: Client
        """

        return self._soap_client

    @property
    def factory(self):
        """ The internal suds soap client factory.

        :rtype: Factory
        """

        return self.soap_client.factory

    @property
    def service_url(self):
        """ The wsdl url of service based on the specific service and environment.

        :rtype: str
        """

        key = (self._service, self._environment)
        service_info_dict = ServiceClient._get_service_info_dict(self._version)
        if key not in service_info_dict:
            raise ValueError(str.format('Cannot find version: [v{0}] service: [{1}] under environment: [{2}]. \
            Please notice that campaign management, bulk, ad intelligence and optimizer services were deprecated in v9',
                                        self._version, self._input_service, self._input_environment))
        return service_info_dict[(self._service, self._environment)].url


    @property
    def refresh_oauth_tokens_automatically(self):
        """ A value indicating whether OAuth access and refresh tokens should be refreshed automatically upon access token expiration.

        :rtype: bool
        """
        return self._refresh_oauth_tokens_automatically

    @refresh_oauth_tokens_automatically.setter
    def refresh_oauth_tokens_automatically(self, value):
        self._refresh_oauth_tokens_automatically = value

    @staticmethod
    def _ensemble_header(authorization_data, **kwargs):
        """ Ensemble the request header send to API services.

        :param authorization_data: the authorization data
        :type authorization_data: AuthorizationData
        :return: the ensemble request header
        :rtype: dict
        """

        if 'soapheaders' in kwargs:
            raise Exception('cannot pass in kwargs contains soapheaders')
        if authorization_data is None:
            return kwargs
        headers = {
            'DeveloperToken': authorization_data.developer_token,
            'CustomerId': str(authorization_data.customer_id),
            'CustomerAccountId': str(authorization_data.account_id),
        }
        authorization_data.authentication.enrich_headers(headers)

        http_headers = {
            'User-Agent': USER_AGENT,
        }

        kwargs['soapheaders'] = headers
        kwargs['headers'] = http_headers

        return kwargs

    @staticmethod
    def _is_expired_token_exception(ex):
        if isinstance(ex, WebFault):
            if hasattr(ex.fault, 'detail') \
                    and hasattr(ex.fault.detail, 'AdApiFaultDetail') \
                    and hasattr(ex.fault.detail.AdApiFaultDetail, 'Errors') \
                    and hasattr(ex.fault.detail.AdApiFaultDetail.Errors, 'AdApiError'):
                ad_api_errors = ex.fault.detail.AdApiFaultDetail.Errors.AdApiError
                if type(ad_api_errors) == list:
                    for ad_api_error in ad_api_errors:
                        if ad_api_error.Code == '109':
                            return True
                else:
                    if ad_api_errors.Code == '109':
                        return True
        return False

    @staticmethod
    def _format_service(service):
        """ Regularize the service name.

        The regularized service name contains only lower character without spaces.

        :param service: the service name
        :type service: str
        :return: the regularized service name
        :rtype: str
        """

        service = service.strip().lower()
        service = service.replace('_', '')
        service = service.replace('-', '')
        service = service.replace(' ', '')
        if service.endswith('service'):
            service = service.replace('service', '')  # remove postfix "service" if any
        return service

    @staticmethod
    def _format_version(version):
        """
        format the version to a int value.
        :param version:
        :return: int version
        """
        if version == 'v9' or version == 9:
            version = 9
        elif version == 'v10' or version == 10:
            version = 10
        else:
            raise ValueError(str.format('version error: [{0}] is not supported.', version))
        return version


    @staticmethod
    def _get_service_info_dict(version):
        """
        Get the service information dict by version
        :param version:
        :return: the service info dict
        """
        if version == 9:
            return SERVICE_INFO_DICT
        elif version == 10:
            return SERVICE_INFO_DICT_V10
        else:
            # Should not run to here, set default to v10
            return SERVICE_INFO_DICT_V10


    @staticmethod
    def _format_environment(environment):
        """ Regularize the environment name.

        the regularized version contains only lower character without spaces.

        :param environment: the environment name
        :type environment: str
        :return: the regularized environment name
        :rtype: str
        """

        environment = environment.strip().lower()
        return environment


class _ServiceCall:
    """ This class wrapped method invocation on ServiceClient, add more logic to suds client call."""

    def __init__(self, service_client, name):
        """ Initializes a new instance of this class.

        :param service_client: the service client need to be wrapped
        :type service_client: ServiceClient
        :param name: the method name
        :type name: str
        :return: the instance of this class
        :rtype: _ServiceCall
        """

        self._service_client = service_client
        self._name = name

    def __call__(self, *args, **kwargs):
        need_to_refresh_token = False
        while True:
            if need_to_refresh_token:
                authentication = self.service_client.authorization_data.authentication
                if not isinstance(authentication, OAuthWithAuthorizationCode):
                    raise ValueError(
                        'The type: {0} of authorization_data cannot refresh token automatically.',
                        type(authentication).__name__
                    )
                refresh_token = authentication.oauth_tokens.refresh_token
                authentication.request_oauth_tokens_by_refresh_token(refresh_token)
                self.service_client.set_options(**self.service_client._options)
            try:
                response = self.service_client.soap_client.service.__getattr__(self.name)(*args, **kwargs)
                return response
            except Exception as ex:
                if need_to_refresh_token is False \
                        and self.service_client.refresh_oauth_tokens_automatically \
                        and self.service_client._is_expired_token_exception(ex):
                    need_to_refresh_token = True
                else:
                    raise ex

    @property
    def service_client(self):
        """ The wrapped service client.

        :rtype: ServiceClient
        """

        return self._service_client

    @property
    def name(self):
        """ The method name.

        :rtype: str
        """

        return self._name


import pkg_resources
import types

from suds.sudsobject import Property
from suds.sax.text import Text

_CAMPAIGN_MANAGEMENT_SERVICE_V10 = Client(
    'file:///' + pkg_resources.resource_filename('bingads', 'v10/proxies/campaign_management_service.xml')
)
_CAMPAIGN_OBJECT_FACTORY_V10 = _CAMPAIGN_MANAGEMENT_SERVICE_V10.factory
# TODO Better to push suds-jurko accept this caching
_CAMPAIGN_OBJECT_FACTORY_V10.object_cache = {}
_CAMPAIGN_OBJECT_FACTORY_V10.create_without_cache = _CAMPAIGN_OBJECT_FACTORY_V10.create


def _suds_objects_deepcopy(origin):
    if origin is None:
        return None
    origin_type = type(origin)
    if origin_type == Text:
        return origin
    if origin_type == list:
        new = []
        for item in origin:
            new.append(_suds_objects_deepcopy(item))
        return new
    if isinstance(origin, Property):
        new = origin_type(None)
        new.__metadata__ = origin.__metadata__
        return new
    new = origin_type()
    for name in origin.__keylist__:
        setattr(new, name, _suds_objects_deepcopy(getattr(origin, name)))
    new.__metadata__ = origin.__metadata__
    return new


def _create_with_cache(self, name):
    if name not in self.object_cache:
        self.object_cache[name] = self.create_without_cache(name)
    obj = self.object_cache[name]
    copied_obj = _suds_objects_deepcopy(obj)
    return copied_obj

_CAMPAIGN_OBJECT_FACTORY_V10.create = types.MethodType(_create_with_cache, _CAMPAIGN_OBJECT_FACTORY_V10)
