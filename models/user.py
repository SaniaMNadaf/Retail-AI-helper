from pydantic import BaseModel, Field, field_validator
from typing import List
import re


def sanitize_text(text: str, max_length: int = 1000) -> str:
    """Sanitize plain text input."""
    if not text:
        return ""
    # Remove control characters except newlines/tabs
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    # Limit length
    return text[:max_length].strip()


class UserProfile(BaseModel):
    name: str = "Aarav Sharma"
    age: int = 25
    height: str = ""
    weight: str = ""
    health: str = "None"
    interests: List[str] = Field(default_factory=list)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = sanitize_text(v, max_length=100)
        if not v:
            raise ValueError("Name cannot be empty")
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters")
        return v

    @field_validator('age')
    @classmethod
    def validate_age(cls, v: int) -> int:
        if not isinstance(v, int) or v < 1 or v > 120:
            raise ValueError("Age must be between 1 and 120")
        return v

    @field_validator('height', 'weight')
    @classmethod
    def validate_measurements(cls, v: str) -> str:
        v = sanitize_text(v, max_length=20)
        if v and not re.match(r'^\d+(\.\d+)?(cm|kg|m|ft|in|lbs?)?$', v, re.IGNORECASE):
            raise ValueError("Invalid format. Use e.g. '178cm' or '72kg'")
        return v

    @field_validator('health')
    @classmethod
    def validate_health(cls, v: str) -> str:
        return sanitize_text(v, max_length=500)

    @field_validator('interests')
    @classmethod
    def validate_interests(cls, v: list[str]) -> list[str]:
        if not isinstance(v, list):
            raise ValueError("Interests must be a list")
        cleaned = []
        for interest in v:
            if isinstance(interest, str):
                cleaned_interest = sanitize_text(interest, max_length=50)
                if cleaned_interest:
                    cleaned.append(cleaned_interest)
        seen = set()
        unique = [x for x in cleaned if not (x in seen or seen.add(x))]
        return unique[:20]
