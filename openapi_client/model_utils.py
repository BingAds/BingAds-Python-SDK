"""Utility functions for model enhancement."""
from pydantic import BaseModel
from typing import Any

def _base_model_getattr(self, item: str) -> Any:
    """Enhanced __getattr__ that supports field aliases."""
    try:
        return object.__getattribute__(self, item)
    except AttributeError:
        # Try to find a field where the alias matches
        for field_name, field in self.model_fields.items():
            if field.alias == item:
                return object.__getattribute__(self, field_name)
        raise

def _base_model_setattr(self, item: str, value: Any) -> None:
    """Enhanced __setattr__ that supports field aliases."""
    # Check if item matches any field aliases
    for field_name, field in self.model_fields.items():
        if field.alias == item:
            object.__setattr__(self, field_name, value)
            return
    object.__setattr__(self, item, value)

def enable_alias_support():
    """
    Enable support for accessing Pydantic model fields via their aliases.
    This should be called before creating any model instances.
    
    Example:
        from openapi_client.model_utils import enable_alias_support
        enable_alias_support()
        
        # Now you can use either style:
        campaign = Campaign()
        campaign.name = "Test"  # Original snake_case
        campaign.Name = "Test"  # Alias PascalCase
    """
    BaseModel.__getattr__ = _base_model_getattr
    BaseModel.__setattr__ = _base_model_setattr