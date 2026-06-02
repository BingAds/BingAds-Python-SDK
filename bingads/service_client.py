import re
import importlib

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

# Pre-compiled patterns — module-level so they are compiled exactly once.
_CAMEL_RE1 = re.compile(r'(.)([A-Z][a-z]+)')
_CAMEL_RE2 = re.compile(r'([a-z0-9])([A-Z])')
_NS_PREFIX_RE = re.compile(r'^ns\d+:')

# Module-level alias — avoids per-call attribute lookup and bypasses any
# class-level __setattr__ override (Pydantic, dataclass, etc.).
_osa = object.__setattr__

def _to_snake_case(name: str) -> str:
    name = _CAMEL_RE1.sub(r'\1_\2', name)
    return _CAMEL_RE2.sub(r'\1_\2', name).lower()


class _CampaignObjectFactoryV13:
    """Factory class for creating campaign management objects."""

    # Maps normalized type_name → resolved class (avoids regex + importlib on every call).
    _class_cache: dict = {}

    # Per-type construction spec: class_ → list of (field_name, attr_name, factory_fn).
    # factory_fn() returns a fresh nested value with no Pydantic validation.
    # Built once per type in _analyze_type(); used by _create_instance() on every call.
    _construct_spec: dict = {}

    # Types with no nested fields AND no custom __init__ side-effects.
    _empty_types: set = set()

    # Types whose __init__ sets discriminator / default fields beyond what the spec covers.
    _needs_init: set = set()

    # Cached ArrayHolder classes per element-type name.
    _array_holder_cache: dict = {}

    # Per-type template instance built once in _analyze_type().
    _template_cache: dict = {}

    # Pre-compiled creator functions: type_name str → callable() → fresh instance.
    # Bypasses all per-call overhead after the first resolution.
    _creator_cache: dict = {}

    # Same but keyed by class object — used by nested-field factories.
    _class_to_creator: dict = {}

    @staticmethod
    def _convert_to_snake_case(name: str) -> str:
        return _to_snake_case(name)

    @classmethod
    def _make_array_holder(cls, element_type: str):
        """Return a new ArrayHolder instance using a cached per-element-type class."""
        holder_class = cls._array_holder_cache.get(element_type)
        if holder_class is None:
            _et = element_type

            class ArrayHolder(list):
                def __init__(self):
                    super().__init__()
                    self._is_none = False

                def __getattr__(self, name):
                    if name.lower() in (_et.lower(), 'long'):
                        return None if self._is_none else self
                    raise AttributeError(name)

                def __setattr__(self, name, value):
                    if name == '_is_none':
                        super().__setattr__(name, value)
                    elif name.lower() in (_et.lower(), 'long'):
                        self._is_none = (value is None)
                        self.clear()
                        if not self._is_none and value is not None:
                            self.extend(value)
                    else:
                        super().__setattr__(name, value)

                def append(self, value):
                    super().append(value)

                def extend(self, values):
                    super().extend(values)

                def clear(self):
                    while len(self):
                        self.pop()

            holder_class = ArrayHolder
            cls._array_holder_cache[element_type] = holder_class
        inst = list.__new__(holder_class)
        _osa(inst, '_is_none', False)
        return inst

    @classmethod
    def _resolve_element_type_name(cls, element_type) -> Optional[str]:
        """Extract the string type name from a List element type annotation."""
        if hasattr(element_type, '__name__'):
            return element_type.__name__
        if hasattr(element_type, '__origin__'):
            if hasattr(element_type.__origin__, '__name__'):
                name = element_type.__origin__.__name__
                if isinstance(element_type, dict) and element_type.get('long'):
                    return 'string'
                return name
        else:
            type_str = str(element_type)
            if 'models' in type_str:
                parts = type_str.split('.')
                return parts[-1].rstrip("']")
        return None

    @classmethod
    def _analyze_type(cls, class_):
        """Build the construction spec for *class_* (runs once per type).

        Calls class_() once to detect any custom __init__ side-effects (e.g.
        ConversionGoal sets its Type discriminator), then walks model_fields to
        record a factory lambda for each nested BaseModel or ArrayHolder field.

        Subsequent _create_instance() calls use this spec with model_construct()
        — no Pydantic validation, no deepcopy.
        """
        try:
            probe = class_()
        except Exception:
            probe = class_.model_construct()

        init_fields = frozenset(probe.model_fields_set)

        spec = []
        spec_field_names = set()

        for field_name, field_info in class_.model_fields.items():
            field_type = field_info.annotation
            factory = None
            try:
                # Unwrap Optional[T] → T
                if hasattr(field_type, '__origin__') and field_type.__origin__ is Union:
                    args = [t for t in field_type.__args__ if t is not type(None)]
                    if not args:
                        continue
                    field_type = args[0]

                if hasattr(field_type, '__origin__') and str(field_type).startswith('typing.List'):
                    element_type = field_type.__args__[0]
                    if hasattr(element_type, '__origin__') and element_type.__origin__ is Union:
                        element_type = next(
                            (t for t in element_type.__args__ if t is not type(None)),
                            element_type,
                        )
                    if hasattr(element_type, 'mro') and Enum in element_type.mro():
                        continue

                    element_type_name = cls._resolve_element_type_name(element_type)
                    if element_type_name:
                        if element_type_name in ('str', 'long'):
                            element_type_name = 'string'
                        _atn = f"ArrayOf{element_type_name}"
                        # Validate the array type exists, then use _make_array_holder
                        # directly — avoids full create() overhead (regex, cache lookup)
                        # on every subsequent call.
                        try:
                            cls.create(_atn)
                            _et = element_type_name
                            factory = lambda et=_et: cls._make_array_holder(et)
                        except ValueError:
                            factory = lambda: []
                    else:
                        factory = lambda: []

                elif isinstance(field_type, type) and issubclass(field_type, BaseModel):
                    _nc = field_type
                    factory = lambda nc=_nc: cls._create_from_class(nc)

            except (AttributeError, IndexError, TypeError, StopIteration):
                continue

            if factory is not None:
                attr_name = _to_snake_case(field_info.alias or field_name)
                spec.append((field_name, attr_name, factory))
                spec_field_names.add(field_name)

        cls._construct_spec[class_] = spec

        # If __init__ sets fields the spec doesn't cover, those fields carry discriminator
        # or default values that model_construct() would miss — fall back to class_().
        if init_fields - spec_field_names:
            cls._needs_init.add(class_)
        elif not spec:
            cls._empty_types.add(class_)

        # Build the per-type template once.  For _needs_init types reuse probe (already
        # created by class_() above); otherwise start from model_construct().  Then
        # populate all spec fields so the template is fully initialised.
        template = probe if class_ in cls._needs_init else class_.model_construct()
        for field_name, attr_name, factory in spec:
            value = factory()
            template.model_fields_set.add(field_name)
            object.__setattr__(template, attr_name, value)
        cls._template_cache[class_] = template

        # Build and cache a pre-compiled creator for this class.
        cls._build_creator(class_)

    @classmethod
    def _build_creator(cls, class_):
        """Build and cache a zero-overhead creator function for *class_*.

        Captures template state in closure variables so each subsequent call
        is: object.__new__ + dict.copy() + set.copy() — no Pydantic Rust
        overhead, no dict lookups for template/spec.
        """
        template = cls._template_cache[class_]
        spec = cls._construct_spec.get(class_, ())

        td = template.__dict__
        tfs = template.__pydantic_fields_set__
        try:
            extra = template.__pydantic_extra__
        except AttributeError:
            extra = None
        try:
            private = template.__pydantic_private__
        except AttributeError:
            private = None

        if not spec:
            def creator(c=class_, td=td, tfs=tfs, e=extra, p=private):
                inst = object.__new__(c)
                _osa(inst, '__dict__', td.copy())
                _osa(inst, '__pydantic_fields_set__', tfs.copy())
                _osa(inst, '__pydantic_extra__', e)
                _osa(inst, '__pydantic_private__', p)
                return inst
        else:
            spec_pairs = tuple((attr, fac) for _, attr, fac in spec)

            def creator(c=class_, td=td, tfs=tfs, e=extra, p=private, sp=spec_pairs):
                inst = object.__new__(c)
                d = td.copy()
                for attr, fac in sp:
                    d[attr] = fac()
                _osa(inst, '__dict__', d)
                _osa(inst, '__pydantic_fields_set__', tfs.copy())
                _osa(inst, '__pydantic_extra__', e)
                _osa(inst, '__pydantic_private__', p)
                return inst

        cls._class_to_creator[class_] = creator
        cls._creator_cache[class_.__name__] = creator
        return creator

    @classmethod
    def _create_from_class(cls, class_):
        """Return a fresh instance for *class_*, using cached creator if available."""
        creator = cls._class_to_creator.get(class_)
        if creator is not None:
            return creator()
        cls._analyze_type(class_)
        return cls._class_to_creator[class_]()

    @classmethod
    def _create_instance(cls, class_):
        """Return a fresh instance by copying the cached template.

        Kept for backward compatibility; hot path now goes through _creator_cache.
        Uses __new__ + dict.copy() instead of model_copy() to bypass Pydantic overhead.
        """
        creator = cls._class_to_creator.get(class_)
        if creator is not None:
            return creator()
        cls._analyze_type(class_)
        return cls._class_to_creator[class_]()

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
        # Ultra-fast path: pre-compiled creator bypasses all resolution overhead.
        creator = cls._creator_cache.get(type_name)
        if creator is not None:
            return creator()

        try:
            original_name = type_name
            type_name = _NS_PREFIX_RE.sub('', type_name)

            if type_name == 'KeyValuePairOfstringstring':
                type_name = 'KeyValuePairOfstringAndstring'

            if type_name.startswith('ArrayOf'):
                element_type = type_name[len('ArrayOf'):]
                # Cache a creator for this ArrayOf* type so future calls hit fast path.
                _et = element_type
                array_creator = lambda et=_et: cls._make_array_holder(et)
                cls._creator_cache[type_name] = array_creator
                if original_name != type_name:
                    cls._creator_cache[original_name] = array_creator
                return array_creator()

            module_name = _to_snake_case(type_name)
            module = importlib.import_module(f"openapi_client.models.campaign.{module_name}")
            class_ = getattr(module, type_name)

            # For Enum types, provide PascalCase access
            if issubclass(class_, Enum):
                class EnumAccessor:
                    def __init__(self, enum_class):
                        self._enum_class = enum_class

                    def __getattr__(self, name):
                        try:
                            return getattr(self._enum_class, name)
                        except AttributeError:
                            try:
                                return getattr(self._enum_class, name.upper())
                            except AttributeError:
                                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

                    def __str__(self):
                        return str(self._enum_class)

                accessor = EnumAccessor(class_)
                # Enum accessors are stateless — return the same singleton each time.
                enum_creator = lambda a=accessor: a
                cls._creator_cache[type_name] = enum_creator
                if original_name != type_name:
                    cls._creator_cache[original_name] = enum_creator
                return accessor

            # Handle KeyValuePair creation with default values and dict-style access
            if type_name == 'KeyValuePairOfstringAndstring':
                instance = class_(Key="", Value="")

                if hasattr(instance, 'model_fields_set'):
                    instance.model_fields_set.update({"Key", "Value"})
                else:
                    instance.model_fields_set = {"Key", "Value"}

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

                for name, method in {
                    '__getitem__': __getitem__,
                    '__setitem__': __setitem__,
                    '__contains__': __contains__,
                    'keys': keys,
                    'values': values,
                    'items': items,
                }.items():
                    setattr(instance.__class__, name, method)
                return instance

            # Cache class for backward compat (keeps _class_cache consistent).
            cls._class_cache[type_name] = class_
            if original_name != type_name:
                cls._class_cache[original_name] = class_

            # Build pre-compiled creator, cache under both string keys.
            cls._analyze_type(class_)
            creator = cls._class_to_creator[class_]
            cls._creator_cache[type_name] = creator
            if original_name != type_name:
                cls._creator_cache[original_name] = creator

            return creator()
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

        self._authorization_data = authorization_data

        # Create configuration with current auth data
        config = Configuration(host=host)

        api_client = ApiClient(configuration=config)

        self._version = self._format_version(version)

        # Set up default headers with our auth headers
        self._set_rest_headers(api_client)

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

    def create_rest_headers(self):
        """ Creates headers for REST API calls.

        :return: Dictionary containing all required headers
        :rtype: dict
        """
        authorization_data = self._authorization_data
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

    def _set_rest_headers(self, api_client):
        headers = self.create_rest_headers()
        for header_name, header_value in headers.items():
            api_client.set_default_header(header_name, header_value)

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
        def with_refreshed_headers(attribute):
            if not callable(attribute):
                return attribute

            def refreshed_call(*args, **kwargs):
                self._set_rest_headers(self._api.api_client)
                return attribute(*args, **kwargs)

            return refreshed_call

        # If name is already in snake_case, try to get it directly
        if not name[0].isupper():
            try:
                return with_refreshed_headers(getattr(self._api, name))
            except AttributeError:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

        # If name is PascalCase, convert to snake_case and try once
        snake_name = _CampaignObjectFactoryV13._convert_to_snake_case(name)
        try:
            return with_refreshed_headers(getattr(self._api, snake_name))
        except AttributeError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

