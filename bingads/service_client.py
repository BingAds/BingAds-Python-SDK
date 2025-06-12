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

    @staticmethod
    def _convert_to_snake_case(name):
        """Converts PascalCase to snake_case.

        Args:
            name: String in PascalCase

        Returns:
            String in snake_case
        """
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

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
        try:
            # Strip namespace prefix and map type names
            import re
            type_name = re.sub(r'^ns\d+:', '', type_name)
            
            # Handle type name mapping
            if type_name == 'KeyValuePairOfstringstring':
                type_name = 'KeyValuePairOfstringAndstring'
            elif type_name == 'Date':
                type_name = 'ModelDate'
            
            # Handle array types
            if type_name.startswith('ArrayOf'):
                element_type = type_name[len('ArrayOf'):]
                # Create a class that holds the array
                class ArrayHolder(list):
                    def __init__(self):
                        super().__init__()
                        # Initialize internal list
                        self._internal_list = []
                        
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

            instance = class_()

            # Special handling for fields in models
            if isinstance(instance, BaseModel):
                for field_name, field_info in instance.model_fields.items():
                    field_type = field_info.annotation
                    field_value = None

                    try:
                        # Check if it's Optional
                        original_type = field_type
                        if hasattr(field_type, '__origin__') and field_type.__origin__ is Union:
                            # Get the non-None type from Union
                            field_type = [t for t in field_type.__args__ if t != type(None)][0]
                        
                        # Handle List types
                        if (hasattr(field_type, '__origin__') and str(field_type).startswith('typing.List')):
                            # Get the element type
                            element_type = field_type.__args__[0]
                            if hasattr(element_type, '__origin__') and element_type.__origin__ is Union:
                                # Handle Optional elements in list
                                element_type = [t for t in element_type.__args__ if t != type(None)][0]
                            
                            # Check if element type is an Enum
                            if hasattr(element_type, 'mro') and Enum in element_type.mro():
                                # For enum lists, respect the default None value
                                continue
                            
                            # For non-enum lists, proceed with array holder creation
                            element_type_name = None
                            
                            if hasattr(element_type, '__name__'):
                                # Simple types like str, int
                                element_type_name = element_type.__name__
                            elif hasattr(element_type, '__origin__'):
                                # Annotated types
                                if hasattr(element_type.__origin__, '__name__'):
                                    element_type_name = element_type.__origin__.__name__
                                    # Handle dictionary format with 'long' type
                                    if isinstance(element_type, dict) and element_type.get('long'):
                                        element_type_name = 'string'
                            else:
                                # Complex types like Setting, Campaign
                                type_str = str(element_type)
                                if 'models' in type_str:
                                    type_parts = type_str.split('.')
                                    element_type_name = type_parts[-1].rstrip("']")
                            
                            if element_type_name:
                                if element_type_name in ('str', 'long'):
                                    element_type_name = 'string'
                                array_type_name = f"ArrayOf{element_type_name}"
                                try:
                                    # Try to create array holder
                                    field_value = cls.create(array_type_name)
                                except ValueError:
                                    # Fall back to regular list
                                    field_value = []
                            else:
                                # If we can't determine the type, use regular list
                                field_value = []
                        else:
                            # Handle non-List types
                            # For custom classes (Pydantic models), create a new instance
                            if isinstance(field_type, type) and issubclass(field_type, BaseModel):
                                type_name = field_type.__name__
                                try:
                                    field_value = cls.create(type_name)
                                except ValueError:
                                    # If creation fails, leave as None
                                    pass
                            elif hasattr(field_type, '__origin__') and field_type.__origin__ is Union:
                                # For Union types (like Optional[BaseModel])
                                non_none_type = [t for t in field_type.__args__ if t != type(None)][0]
                                if isinstance(non_none_type, type) and issubclass(non_none_type, BaseModel):
                                    type_name = non_none_type.__name__
                                    try:
                                        field_value = cls.create(type_name)
                                    except ValueError:
                                        # If creation fails, leave as None
                                        pass

                    except (AttributeError, IndexError, TypeError):
                        continue

                    if field_value is not None:
                        # Set PascalCase and snake_case version
                        pascal_case = field_info.alias or field_name
                        snake_case = cls._convert_to_snake_case(pascal_case)
                        
                        # Use model_fields_set to track initialized fields
                        instance.model_fields_set.add(field_name)
                        setattr(instance, snake_case, field_value)

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

