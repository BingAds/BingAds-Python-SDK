from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel

from openapi_client.api.campaign_management_service_api import CampaignManagementServiceApi
from openapi_client.api.bulk_service_api import BulkServiceApi
from openapi_client.api.reporting_service_api import ReportingServiceApi
from openapi_client.api.customer_management_service_api import CustomerManagementServiceApi
from openapi_client.api.customer_billing_service_api import CustomerBillingServiceApi
from openapi_client.api.ad_insight_service_api import AdInsightServiceApi
from openapi_client.model_utils import enable_alias_support
from openapi_client.configuration import Configuration
from openapi_client.api_client import ApiClient
from .manifest import USER_AGENT
import importlib

class _CampaignObjectFactoryV13:
    """Factory class for creating campaign management objects."""

    # Per-type template cache: maps class → a fully-initialized instance that is
    # deep-copied on each create() call.  Built once on first use, reused after.
    _template_cache: dict = {}

    # Types whose template has no pre-built nested fields (all fields are None/primitives).
    # For these, model_construct() is called directly — no deepcopy needed.
    _empty_types: set = set()

    # Maps normalized type_name → resolved class (avoids regex + importlib on every call).
    _class_cache: dict = {}

    @staticmethod
    def _convert_to_snake_case(name):
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    @classmethod
    def _build_template(cls, class_):
        """Build one fully-initialized template instance (slow path, runs once per type).

        Uses class_() so that custom __init__ logic (e.g. ConversionGoal setting the
        Type discriminator) is preserved, then pre-initialises nested BaseModel fields
        and ArrayHolder wrappers.  This runs once per type; subsequent create() calls
        return a cheap deepcopy of the cached result.
        """
        instance = class_()
        for field_name, field_info in class_.model_fields.items():
            field_type = field_info.annotation
            field_value = None
            try:
                if hasattr(field_type, '__origin__') and field_type.__origin__ is Union:
                    field_type = [t for t in field_type.__args__ if t != type(None)][0]

                if hasattr(field_type, '__origin__') and str(field_type).startswith('typing.List'):
                    element_type = field_type.__args__[0]
                    if hasattr(element_type, '__origin__') and element_type.__origin__ is Union:
                        element_type = [t for t in element_type.__args__ if t != type(None)][0]
                    if hasattr(element_type, 'mro') and Enum in element_type.mro():
                        continue
                    element_type_name = None
                    if hasattr(element_type, '__name__'):
                        element_type_name = element_type.__name__
                    elif hasattr(element_type, '__origin__'):
                        if hasattr(element_type.__origin__, '__name__'):
                            element_type_name = element_type.__origin__.__name__
                            if isinstance(element_type, dict) and element_type.get('long'):
                                element_type_name = 'string'
                    else:
                        type_str = str(element_type)
                        if 'models' in type_str:
                            type_parts = type_str.split('.')
                            element_type_name = type_parts[-1].rstrip("']")
                    if element_type_name:
                        if element_type_name in ('str', 'long'):
                            element_type_name = 'string'
                        try:
                            field_value = cls.create(f"ArrayOf{element_type_name}")
                        except ValueError:
                            field_value = []
                    else:
                        field_value = []
                elif isinstance(field_type, type) and issubclass(field_type, BaseModel):
                    try:
                        field_value = cls._get_template(field_type)
                    except Exception:
                        pass
                elif hasattr(field_type, '__origin__') and field_type.__origin__ is Union:
                    non_none_type = [t for t in field_type.__args__ if t != type(None)][0]
                    if isinstance(non_none_type, type) and issubclass(non_none_type, BaseModel):
                        try:
                            field_value = cls._get_template(non_none_type)
                        except Exception:
                            pass
            except (AttributeError, IndexError, TypeError):
                continue

            if field_value is not None:
                pascal_case = field_info.alias or field_name
                snake_case = cls._convert_to_snake_case(pascal_case)
                instance.model_fields_set.add(field_name)
                object.__setattr__(instance, snake_case, field_value)
        return instance

    @classmethod
    def _get_template(cls, class_):
        """Return the cached template for *class_*, building it on first call."""
        if class_ not in cls._template_cache:
            template = cls._build_template(class_)
            cls._template_cache[class_] = template
            # If _build_template set no fields, all fields are None/primitives.
            # We can skip deepcopy on every call and just use model_construct().
            if not template.model_fields_set:
                cls._empty_types.add(class_)
        return cls._template_cache[class_]

    @classmethod
    def _create_instance(cls, class_):
        """Return a fresh instance: class_() for simple types, deepcopy for nested."""
        if class_ in cls._empty_types:
            return class_()
        import copy
        return copy.deepcopy(cls._get_template(class_))

    @classmethod
    def create(cls, type_name):
        """Creates an instance of the specified type.

        Args:
            type_name: Name of the type to create (in PascalCase)

        Returns:
            Instance of the requested type

        Raises:
            ValueError: If type_name is not supported
        """
        # Fast path: type already resolved on a previous call.
        cached = cls._class_cache.get(type_name)
        if cached is not None:
            return cls._create_instance(cached)

        try:
            original_name = type_name
            # Strip namespace prefix and map type names
            import re
            type_name = re.sub(r'^ns\d+:', '', type_name)

            # Handle type name mapping
            if type_name == 'KeyValuePairOfstringstring':
                type_name = 'KeyValuePairOfstringAndstring'

            # Handle array types (not cached — each ArrayHolder is a one-shot closure)
            if type_name.startswith('ArrayOf'):
                element_type = type_name[len('ArrayOf'):]
                # Create a class that holds the array
                class ArrayHolder(list):
                    def __init__(self):
                        super().__init__()
                        # Initialize internal list and None flag
                        self._internal_list = []
                        self._is_none = False

                    def __getattr__(self, name):
                        # Support both cases (e.g. both 'string' and 'String')
                        # Also handle 'long' as 'string'
                        if name.lower() in (element_type.lower(), 'long'):
                            return None if self._is_none else self
                        raise AttributeError(name)

                    def __setattr__(self, name, value):
                        if name in ('_internal_list', '_is_none'):
                            super().__setattr__(name, value)
                        elif name.lower() in (element_type.lower(), 'long'):
                            self._is_none = (value is None)
                            # Update list contents
                            self.clear()
                            if not self._is_none and value is not None:
                                self.extend(value)
                        else:
                            super().__setattr__(name, value)

                    # List interface implementation
                    def append(self, value):
                        super().append(value)

                    def extend(self, values):
                        super().extend(values)

                    def clear(self):
                        while len(self):
                            self.pop()

                return ArrayHolder()

            module_name = cls._convert_to_snake_case(type_name)
            module = importlib.import_module(f"openapi_client.models.campaign.{module_name}")
            class_ = getattr(module, type_name)

            # For Enum types, provide PascalCase access
            if issubclass(class_, Enum):
                class EnumAccessor:
                    def __init__(self, enum_class):
                        self._enum_class = enum_class

                    def __getattr__(self, name):
                        try:
                            # Try to get the enum value directly
                            return getattr(self._enum_class, name)
                        except AttributeError:
                            try:
                                # Try uppercase version if PascalCase fails
                                return getattr(self._enum_class, name.upper())
                            except AttributeError:
                                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

                    def __str__(self):
                        return str(self._enum_class)

                return EnumAccessor(class_)

            # Handle KeyValuePair creation with default values and dict-style access
            if type_name == 'KeyValuePairOfstringAndstring':
                # Create instance with required fields and proper model initialization
                instance = class_(Key="", Value="")

                # Ensure model fields are properly tracked
                if hasattr(instance, 'model_fields_set'):
                    instance.model_fields_set.add("Key")
                    instance.model_fields_set.add("Value")
                else:
                    instance.model_fields_set = {"Key", "Value"}

                # Add dict-style access methods
                def __getitem__(self, key):
                    if key.lower() == 'key':
                        return self.Key
                    elif key.lower() == 'value':
                        return self.Value
                    raise KeyError(key)
                
                def __setitem__(self, key, value):
                    if key.lower() == 'key':
                        self.Key = value
                    elif key.lower() == 'value':
                        self.Value = value
                    else:
                        raise KeyError(key)

                def __contains__(self, key):
                    return key.lower() in ('key', 'value')

                def keys(self):
                    return ['key', 'value']

                def values(self):
                    return [self.Key, self.Value]

                def items(self):
                    return [('key', self.Key), ('value', self.Value)]
                
                # Add dict-style access to the instance's class
                methods = {
                    '__getitem__': __getitem__,
                    '__setitem__': __setitem__,
                    '__contains__': __contains__,
                    'keys': keys,
                    'values': values,
                    'items': items
                }
                
                for name, method in methods.items():
                    setattr(instance.__class__, name, method)
                return instance

            instance = cls._create_instance(class_)
            # Cache under both the original call-site name and the normalized name so
            # callers using namespace prefixes (e.g. 'ns3:HotelGroup') also hit the fast path.
            cls._class_cache[type_name] = class_
            if original_name != type_name:
                cls._class_cache[original_name] = class_

            return instance
        except (ImportError, AttributeError):
            raise ValueError(f"Type '{type_name}' is not supported")

# this is used to create entity only.
_CAMPAIGN_OBJECT_FACTORY_V13 = _CampaignObjectFactoryV13()

class ServiceClient:
    """ Provides an interface for calling the methods of the specified Bing Ads service."""
    endpoints = {
        'sandbox': {
            'adinsight': 'https://adinsight.api.sandbox.bingads.microsoft.com',
            'campaignmanagement': 'https://campaign.api.sandbox.bingads.microsoft.com',
            'bulk': 'https://bulk.api.sandbox.bingads.microsoft.com',
            'customerbilling': 'https://clientcenter.api.sandbox.bingads.microsoft.com',
            'customermanagement': 'https://clientcenter.api.sandbox.bingads.microsoft.com',
            'reporting': 'https://reporting.api.sandbox.bingads.microsoft.com'
        },
        'production': {
            'adinsight': 'https://adinsight.api.bingads.microsoft.com',
            'campaignmanagement': 'https://campaign.api.bingads.microsoft.com',
            'bulk': 'https://bulk.api.bingads.microsoft.com',
            'customerbilling': 'https://clientcenter.api.bingads.microsoft.com',
            'customermanagement': 'https://clientcenter.api.bingads.microsoft.com',
            'reporting': 'https://reporting.api.bingads.microsoft.com'
        }
    }

    def __init__(self, service, version, authorization_data=None, environment='production', location=None, **options):
        """ Initializes a new instance of this class.

        :param service: The service name.
        :type service: str
        :param authorization_data: (optional) The authorization data, if not provided, cannot call operations on service
        :type authorization_data: AuthorizationData or None
        :param environment: (optional) The environment name, can only be 'production' or 'sandbox', the default is 'production'
        :type environment: str
        :param version: to specify the service version
        """
        # Enable alias for propertyName, both campaign.daily_budget and campaign.DailyBudget work
        enable_alias_support()

        service_name = self._format_service(service)

        if location == None:
            host = self._get_endpoint(environment, service_name)
        else:
            host = location

        # Create configuration with current auth data
        config = Configuration(host=host)

        api_client = ApiClient(configuration=config)

        self._version = self._format_version(version)

        # Set up default headers with our auth headers
        headers = self.create_rest_headers(authorization_data)
        for header_name, header_value in headers.items():
            api_client.set_default_header(header_name, header_value)

        if (service_name == 'campaignmanagement'):
            self._api = CampaignManagementServiceApi(api_client)
        elif (service_name == 'bulk'):
            self._api = BulkServiceApi(api_client)
        elif (service_name == 'reporting'):
            self._api = ReportingServiceApi(api_client)
        elif (service_name == 'customermanagement'):
            self._api = CustomerManagementServiceApi(api_client)
        elif (service_name == 'customerbilling'):
            self._api = CustomerBillingServiceApi(api_client)
        elif (service_name == 'adinsight'):
            self._api = AdInsightServiceApi(api_client)

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

    def create_rest_headers(self, authorization_data):
        """ Creates headers for REST API calls.

        :param authorization_data: Authorization data for the request
        :type authorization_data: AuthorizationData
        :return: Dictionary containing all required headers
        :rtype: dict
        """
        if authorization_data is None:
            raise ValueError("Authorization data cannot be None.")

        headers = {
            'CustomerAccountId': str(authorization_data.account_id),
            'CustomerId': str(authorization_data.customer_id),
            'DeveloperToken': authorization_data.developer_token,
            'User-Agent': USER_AGENT,
        }

        # Add authentication headers (either OAuth Bearer token or username/password)
        authorization_data.authentication.enrich_headers(headers)

        return headers

    @staticmethod
    def _format_version(version):
        """
        format the version to a int value.
        :param version:
        :return: int version
        """
        if version == 'v13' or version == 13:
            return 13
        raise ValueError(str.format('version error: [{0}] is not supported.', version))

    @staticmethod
    def _get_endpoint(env, service):
        return ServiceClient.endpoints.get(env, {}).get(service, None)

    @property
    def factory(self):
        """Returns the appropriate object factory for campaign objects."""
        return _CAMPAIGN_OBJECT_FACTORY_V13

    def get_response_header(self):
        """Gets the headers from the last API call response.

        Returns:
            dict: Dictionary containing response headers
        """
        if hasattr(self._api, 'api_client') and hasattr(self._api.api_client, 'last_response'):
            return self._api.api_client.last_response.headers
        return {}

    def __getattr__(self, name):
        """Delegate method calls to the underlying API instance.
        Supports both snake_case and PascalCase method names."""
        # If name is already in snake_case, try to get it directly
        if not name[0].isupper():
            try:
                return getattr(self._api, name)
            except AttributeError:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

        # If name is PascalCase, convert to snake_case and try once
        snake_name = _CampaignObjectFactoryV13._convert_to_snake_case(name)
        try:
            return getattr(self._api, snake_name)
        except AttributeError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

