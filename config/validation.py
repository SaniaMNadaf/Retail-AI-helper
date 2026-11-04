import re
from enum import Enum
from typing import Optional
from pydantic import BaseModel, field_validator, ValidationError
from config.settings import (
    API_KEY,
    DEFAULT_GEMINI_MODEL,
    PAGE_LOGO,
    PAGE_LOGIN,
    PAGE_REGISTER,
    PAGE_CLONING,
    PAGE_HOME,
)


class PageRoute(str, Enum):
    """Enum for all valid page routes."""
    LOGO = PAGE_LOGO
    LOGIN = PAGE_LOGIN
    REGISTER = PAGE_REGISTER
    CLONING = PAGE_CLONING
    HOME = PAGE_HOME

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value in cls._value2member_map_

    @classmethod
    def get_default(cls) -> "PageRoute":
        return cls.LOGO


class NavItem(str, Enum):
    """Enum for navigation items."""
    DASHBOARD = "Dashboard"
    SCANNER = "AI Scanner"
    TWIN = "Digital Twin"
    RECORDS = "Scan History"
    SETTINGS = "Settings"

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value in cls._value2member_map_

    @classmethod
    def get_default(cls) -> "NavItem":
        return cls.DASHBOARD


class AppConfig(BaseModel):
    """Validated application configuration."""
    
    api_key: str
    gemini_model: str = DEFAULT_GEMINI_MODEL
    
    @field_validator('api_key')
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("GOOGLE_API_KEY is required but not set in environment")
        # Basic format validation for Google API keys
        if not re.match(r'^[A-Za-z0-9_-]{20,}$', v.strip()):
            raise ValueError("GOOGLE_API_KEY appears to be invalid format")
        return v.strip()
    
    @field_validator('gemini_model')
    @classmethod
    def validate_gemini_model(cls, v: str) -> str:
        valid_models = [
            "gemini-2.5-flash",
            "gemini-2.5-pro",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
        ]
        if v not in valid_models:
            raise ValueError(f"Invalid Gemini model. Must be one of: {valid_models}")
        return v


def validate_config() -> AppConfig:
    """
    Validate and return application configuration.
    Raises ValidationError if configuration is invalid.
    """
    return AppConfig(
        api_key=API_KEY,
        gemini_model=DEFAULT_GEMINI_MODEL,
    )


def get_validated_page(page: str) -> PageRoute:
    """Get validated page route, fallback to default."""
    if PageRoute.is_valid(page):
        return PageRoute(page)
    return PageRoute.get_default()


def get_validated_nav(nav: str) -> NavItem:
    """Get validated navigation item, fallback to default."""
    if NavItem.is_valid(nav):
        return NavItem(nav)
    return NavItem.get_default()


class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass


def check_required_config() -> None:
    """Check all required configuration at startup. Raises ConfigError if invalid."""
    try:
        validate_config()
    except ValidationError as e:
        errors = []
        for error in e.errors():
            field = " -> ".join(str(x) for x in error['loc'])
            msg = error['msg']
            errors.append(f"{field}: {msg}")
        raise ConfigError(f"Configuration validation failed:\n" + "\n".join(errors))