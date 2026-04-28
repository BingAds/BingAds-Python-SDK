"""
REST to SOAP Adapter Module

This module provides automatic conversion of REST-style Pydantic models
to SOAP-compatible proxy objects for use with bulk entity serialization.

The adapter enables users to use modern REST-style models like:
    campaign = Campaign(
        campaign_type=CampaignType.SEARCH,
        languages=['All'],
        ...
    )

Instead of SOAP-style factory-created objects:
    campaign = factory.create('Campaign')
    campaign.CampaignType = ['Search']
    campaign.Languages.string = ['All']
"""

from enum import Flag, Enum
from pydantic import BaseModel
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13


class RestToSoapAdapter:
    """Adapts REST-style Pydantic models to SOAP-compatible proxy objects."""
    
    @staticmethod
    def is_rest_model(obj):
        """
        Check if object is a REST-style Pydantic model.
        
        Args:
            obj: Object to check
            
        Returns:
            bool: True if object is a Pydantic BaseModel instance
        """
        return isinstance(obj, BaseModel)
    
    @staticmethod
    def adapt(obj, target_type=None):
        """
        Convert REST model to SOAP-compatible proxy if needed.
        
        If the object is already a SOAP-style proxy (not a Pydantic model),
        it is returned unchanged for backward compatibility.
        
        Args:
            obj: Object to adapt (REST Pydantic model or SOAP proxy)
            target_type: Optional type name override
            
        Returns:
            SOAP-compatible proxy object
        """
        if obj is None:
            return None
            
        if not RestToSoapAdapter.is_rest_model(obj):
            return obj  # Already SOAP-style, return as-is
        
        # Determine target type from class name
        type_name = target_type or obj.__class__.__name__
        
        try:
            soap_obj = _CAMPAIGN_OBJECT_FACTORY_V13.create(type_name)
        except ValueError:
            # Type not supported by factory, return original
            return obj
        
        # Copy and convert all fields
        RestToSoapAdapter._copy_fields(obj, soap_obj)
        return soap_obj
    
    @staticmethod
    def _copy_fields(rest_obj, soap_obj):
        """
        Copy fields from REST model to SOAP object with conversions.
        
        Args:
            rest_obj: Source Pydantic model
            soap_obj: Target SOAP proxy object
        """
        for field_name, field_info in rest_obj.model_fields.items():
            alias = field_info.alias or field_name
            
            # Get the value using the field name (not alias)
            try:
                value = getattr(rest_obj, field_name, None)
            except AttributeError:
                continue
            
            if value is None:
                continue
            
            # Convert based on value type
            converted = RestToSoapAdapter._convert_value(
                value, 
                alias,
                field_info.annotation
            )
            
            # Set the value on SOAP object using alias (PascalCase)
            try:
                setattr(soap_obj, alias, converted)
            except AttributeError:
                # Field doesn't exist on SOAP object, skip
                pass
    
    @staticmethod
    def _convert_value(value, field_name, type_hint):
        """
        Convert individual values based on their type.
        
        Args:
            value: Value to convert
            field_name: Name of the field (PascalCase alias)
            type_hint: Type annotation from Pydantic model
            
        Returns:
            Converted value suitable for SOAP object
        """
        # Flag enum to list conversion (e.g., CampaignType)
        if isinstance(value, Flag):
            return RestToSoapAdapter._flag_to_list(value)
        
        # Regular enum - extract value
        if isinstance(value, Enum) and not isinstance(value, Flag):
            return value
        
        # List handling - check if needs ArrayOf wrapper
        if isinstance(value, list):
            return RestToSoapAdapter._list_to_array_of(value, field_name)
        
        # Nested Pydantic model
        if isinstance(value, BaseModel):
            return RestToSoapAdapter.adapt(value)
        
        # Primitive types - return as-is
        return value
    
    @staticmethod
    def _flag_to_list(flag_value):
        """
        Convert Flag enum to list of strings (SOAP style).
        
        Example:
            CampaignType.SEARCH | CampaignType.AUDIENCE -> ['Search', 'Audience']
            
        Args:
            flag_value: Flag enum value (possibly combined with bitwise OR)
            
        Returns:
            List of string representations
        """
        if flag_value is None:
            return None
            
        flag_class = type(flag_value)
        result = []
        
        for member in flag_class:
            if member & flag_value:
                # Convert SEARCH -> 'Search', DYNAMICSEARCHADS -> 'DynamicSearchAds'
                string_value = RestToSoapAdapter._flag_name_to_string(member)
                result.append(string_value)
        
        return result if result else None
    
    @staticmethod
    def _flag_name_to_string(flag):
        """
        Convert flag member name to proper case string (generic approach).
        
        This uses the Flag enum's built-in __str__ method which typically contains
        the correct PascalCase representation (e.g., CampaignType.SEARCH -> 'Search').
        
        Fallback: If str(flag) doesn't produce a valid result, convert the uppercase
        name to PascalCase using heuristics.
        
        Args:
            flag: Flag enum member (e.g., CampaignType.SEARCH)
            
        Returns:
            Proper-case string representation (e.g., 'Search')
        """
        # Try using the enum's __str__ method first (which has the correct mapping)
        str_value = str(flag)
        
        # If __str__ returns a valid single word (not the enum name pattern like "CampaignType.SEARCH")
        # and doesn't contain '.' or '|', use it
        if str_value and '.' not in str_value and '|' not in str_value:
            return str_value
        
        # Fallback: Convert UPPERCASE_NAME to PascalCase
        # e.g., DYNAMICSEARCHADS -> DynamicSearchAds
        return RestToSoapAdapter._uppercase_to_pascal_case(flag.name)
    
    @staticmethod
    def _uppercase_to_pascal_case(name):
        """
        Convert an uppercase enum name to PascalCase.
        
        Examples:
            SEARCH -> Search
            DYNAMICSEARCHADS -> Dynamicsearchads (fallback - may not be perfect)
            PERFORMANCE_MAX -> PerformanceMax (if it had underscores)
        
        Args:
            name: Uppercase string (e.g., 'SEARCH', 'DYNAMICSEARCHADS')
            
        Returns:
            PascalCase string
        """
        # Handle underscore-separated names (e.g., PERFORMANCE_MAX -> PerformanceMax)
        if '_' in name:
            return ''.join(word.capitalize() for word in name.split('_'))
        
        # For single words, just capitalize first letter and lowercase rest
        return name.capitalize()
    
    @staticmethod
    def _list_to_array_of(items, field_name):
        """
        Convert Python list to ArrayOf wrapper if needed (generic approach).
        
        This method automatically detects whether a field requires an ArrayOf wrapper
        by attempting to create the wrapper and checking for the appropriate accessor.
        
        For List[str] fields like FinalUrls, Languages -> ArrayOfstring with .string accessor
        For List[Model] fields like Settings -> ArrayOfSetting with .Setting accessor
        
        Args:
            items: List of items to convert
            field_name: Name of the field (PascalCase alias)
            
        Returns:
            ArrayOf wrapper or converted list
        """
        if not items:
            return items
        
        # Convert items recursively first
        converted_items = [
            RestToSoapAdapter.adapt(item) if isinstance(item, BaseModel) else item
            for item in items
        ]
        
        # Determine the item type to guess the ArrayOf wrapper
        first_item = converted_items[0]
        
        # Try to detect and create appropriate wrapper with items
        wrapper = RestToSoapAdapter._try_create_array_wrapper_with_items(
            first_item, converted_items, field_name
        )
        
        if wrapper is not None:
            return wrapper
        
        # No wrapper needed - return plain list
        return converted_items
    
    @staticmethod
    def _try_create_array_wrapper_with_items(sample_item, items, field_name=None):
        """
        Try to create an ArrayOf wrapper and set items.
        
        Strategy:
        1. For strings: use ArrayOfstring with .string accessor
        2. For complex objects, determine accessor based on polymorphism:
           - If item type ends with singular field name AND singular field name is a real base type:
             Use field name based wrapper (ArrayOfSetting with .Setting)
           - Otherwise: use item type based wrapper (ArrayOfTargetSettingDetail with .TargetSettingDetail)
        
        Args:
            sample_item: A sample item to determine type
            items: The converted items to set in the wrapper
            field_name: Name of the field (e.g., 'Settings') to help determine wrapper type
            
        Returns:
            Wrapper with items set, or None if no wrapper needed
        """
        # Case 1: List of strings -> ArrayOfstring
        if isinstance(sample_item, str):
            try:
                wrapper = _CAMPAIGN_OBJECT_FACTORY_V13.create('ArrayOfstring')
                if hasattr(wrapper, 'string'):
                    wrapper.string = items
                    return wrapper
            except (ValueError, Exception):
                pass
            return None
        
        # Get item type name
        item_type_name = RestToSoapAdapter._get_soap_type_name(sample_item)
        
        if field_name and item_type_name:
            singular_name = field_name.rstrip('s') if field_name.endswith('s') else field_name
            
            # Check for polymorphic case: item type ends with singular field name
            # AND the singular name represents a real base type (can be imported as a module)
            # e.g., "TargetSetting" ends with "Setting", and Setting is a real model -> polymorphic
            # e.g., "TargetSettingDetail" ends with "Detail", but Detail is NOT a real model -> not polymorphic
            is_polymorphic_subtype = False
            
            if item_type_name.endswith(singular_name) and item_type_name != singular_name:
                # Check if the singular name represents a real model type
                is_polymorphic_subtype = RestToSoapAdapter._is_real_model_type(singular_name)
            
            if is_polymorphic_subtype:
                # Use field name based wrapper for polymorphic types
                # e.g., Settings with TargetSetting -> ArrayOfSetting with .Setting accessor
                array_type_name = f'ArrayOf{singular_name}'
                try:
                    wrapper = _CAMPAIGN_OBJECT_FACTORY_V13.create(array_type_name)
                    setattr(wrapper, singular_name, items)
                    return wrapper
                except (ValueError, Exception):
                    pass
        
        # Non-polymorphic case or polymorphic failed: use item type based wrapper
        # e.g., Details with TargetSettingDetail -> ArrayOfTargetSettingDetail with .TargetSettingDetail
        if item_type_name:
            array_type_name = f'ArrayOf{item_type_name}'
            try:
                wrapper = _CAMPAIGN_OBJECT_FACTORY_V13.create(array_type_name)
                setattr(wrapper, item_type_name, items)
                return wrapper
            except (ValueError, Exception):
                pass
        
        # Final fallback: field name based wrapper
        if field_name:
            singular_name = field_name.rstrip('s') if field_name.endswith('s') else field_name
            array_type_name = f'ArrayOf{singular_name}'
            try:
                wrapper = _CAMPAIGN_OBJECT_FACTORY_V13.create(array_type_name)
                setattr(wrapper, singular_name, items)
                return wrapper
            except (ValueError, Exception):
                pass
        
        return None
    
    @staticmethod
    def _is_real_model_type(type_name):
        """
        Check if a type name represents a real model type (not just a suffix).
        
        This is used to detect polymorphic base types like 'Setting' which have
        subtypes like 'TargetSetting', 'HotelSetting', etc.
        
        Args:
            type_name: The type name to check (e.g., 'Setting', 'Detail')
            
        Returns:
            True if the type exists as a real model, False otherwise
        """
        import importlib
        import re
        
        # Convert PascalCase to snake_case
        snake_name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', type_name)
        snake_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', snake_name).lower()
        
        try:
            # Try to import the module
            importlib.import_module(f"openapi_client.models.campaign.{snake_name}")
            return True
        except ImportError:
            return False
    
    @staticmethod
    def _get_soap_type_name(obj):
        """
        Get the SOAP type name of an object.
        
        Args:
            obj: Object to inspect
            
        Returns:
            Type name string or None
        """
        # For SOAP proxy objects, check for Type attribute
        if hasattr(obj, 'Type') and isinstance(getattr(obj, 'Type', None), str):
            return obj.Type
        
        # For zeep/suds objects, try to get class name
        type_name = type(obj).__name__
        
        # Skip built-in types
        if type_name in ('str', 'int', 'float', 'bool', 'dict', 'list', 'NoneType'):
            return None
        
        return type_name


def enable_rest_entity_support():
    """
    Enable REST-style Pydantic models to be used with bulk entities.

    This function monkey-patches the property setters of bulk entity classes
    to automatically convert REST models to SOAP-compatible proxies.

    Call this once at module import time to enable the feature globally.

    Example:
        from bingads.v13.internal.rest_adapter import enable_rest_entity_support
        enable_rest_entity_support()

        # Now REST models work with bulk entities:
        from openapi_client.models.campaign import Campaign, CampaignType

        campaign = Campaign(
            campaign_type=CampaignType.SEARCH,
            name="My Campaign"
        )
        bulk_campaign = BulkCampaign()
        bulk_campaign.campaign = campaign  # Automatically adapted!
    """
    # Enable PascalCase alias access on Pydantic models (e.g. model.SupportedCampaignTypes
    # routes to model.supported_campaign_types via the field's alias).
    # Required so bulk entity _MAPPINGS can use PascalCase attribute names on REST models.
    try:
        from openapi_client.model_utils import enable_alias_support
        enable_alias_support()
    except ImportError:
        pass

    _auto_discover_and_patch_bulk_entities()


def _auto_discover_and_patch_bulk_entities():
    """
    Automatically discover all bulk entity classes and patch ALL their settable properties.
    
    This generic approach:
    1. Imports the bulk entities module
    2. Finds all classes starting with 'Bulk'
    3. Patches ALL settable properties (those with both getter and setter)
    4. Runtime detection in the setter determines if adaptation is needed
    
    No property name guessing or mappings required - the setter's runtime check
    using is_rest_model() handles the decision of whether to adapt.
    """
    import inspect
    
    # Import the entities package
    import bingads.v13.bulk.entities as entities_pkg
    
    # Track patched classes for debugging
    patched = []
    
    # Get all modules in the entities package (including subpackages)
    entity_classes = _collect_bulk_entity_classes(entities_pkg)
    
    for cls in entity_classes:
        # Patch ALL settable properties - runtime detection handles the rest
        for name, obj in inspect.getmembers(cls):
            # Skip private/internal attributes
            if name.startswith('_'):
                continue
            
            # Only process property objects with setters
            if isinstance(obj, property) and obj.fset is not None:
                success = _patch_property_setter(cls, name)
                if success:
                    patched.append((cls.__name__, name))
    
    return patched


def _collect_bulk_entity_classes(package):
    """
    Recursively collect all Bulk* classes from a package.
    
    Args:
        package: The package to scan
        
    Returns:
        Set of bulk entity classes
    """
    import pkgutil
    import importlib
    import inspect
    
    classes = set()
    
    # Get path and prefix for submodule iteration
    try:
        package_path = package.__path__
        package_name = package.__name__
    except AttributeError:
        return classes
    
    # Iterate through all modules in the package
    for importer, modname, ispkg in pkgutil.walk_packages(
        path=package_path,
        prefix=package_name + '.',
        onerror=lambda x: None
    ):
        try:
            module = importlib.import_module(modname)
        except ImportError:
            continue
        
        # Find all classes in this module
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Only process classes defined in this module (not imported)
            if obj.__module__ == modname and name.startswith('Bulk'):
                classes.add(obj)
    
    # Also check the package's __init__.py for directly defined classes
    for name, obj in inspect.getmembers(package, inspect.isclass):
        if obj.__module__.startswith(package.__name__) and name.startswith('Bulk'):
            classes.add(obj)
    
    return classes



def _patch_property_setter(cls, prop_name):
    """
    Patch a property setter to auto-adapt REST models.
    
    Args:
        cls: Class to patch
        prop_name: Name of the property
        
    Returns:
        True if successfully patched, False otherwise
    """
    try:
        original_prop = getattr(cls, prop_name, None)
    except Exception:
        return False
    
    if not isinstance(original_prop, property):
        return False
    
    original_getter = original_prop.fget
    original_setter = original_prop.fset
    
    if original_setter is None:
        return False
    
    def adapted_setter(self, value):
        # Convert REST model to SOAP proxy if needed
        adapted_value = RestToSoapAdapter.adapt(value)
        original_setter(self, adapted_value)
    
    # Create new property with adapted setter
    new_prop = property(original_getter, adapted_setter)
    
    try:
        # Replace the property on the class
        setattr(cls, prop_name, new_prop)
        return True
    except Exception:
        return False


# Flag to track if REST support has been enabled
_rest_support_enabled = False


def ensure_rest_support():
    """
    Ensure REST entity support is enabled (idempotent).
    
    Safe to call multiple times - only enables once.
    """
    global _rest_support_enabled
    if not _rest_support_enabled:
        enable_rest_entity_support()
        _rest_support_enabled = True
