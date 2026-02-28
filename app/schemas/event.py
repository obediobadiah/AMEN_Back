import json
from pydantic import BaseModel, ConfigDict, field_validator, ValidationInfo
from datetime import datetime
from typing import Optional, Dict, Union, Any

class EventBase(BaseModel):
    title: Dict[str, str]
    description: Optional[Dict[str, str]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[Dict[str, str]] = None
    status: Optional[str] = None # Upcoming, Past
    registration_link: Optional[str] = None
    category: Optional[str] = None
    thumbnail_url: Optional[str] = None

    @field_validator("*", mode="before")
    @classmethod
    def empty_string_to_none(cls, v: Any, info: ValidationInfo) -> Any:
        if info.field_name == "source_lang":
            return v
        if isinstance(v, str) and not v.strip():
            return None
        return v

    @field_validator("title", "description", "location", mode="before")
    @classmethod
    def parse_legacy_json_or_string(cls, value: Any) -> Optional[Dict[str, str]]:
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                pass
            return {"en": value, "fr": value}
        return value

class EventCreate(BaseModel):
    title: Any
    description: Optional[Any] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[Any] = None
    status: Optional[str] = None
    registration_link: Optional[str] = None
    category: Optional[str] = None
    thumbnail_url: Optional[str] = None
    source_lang: Optional[str] = "fr"

class EventUpdate(BaseModel):
    title: Optional[Any] = None
    description: Optional[Any] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[Any] = None
    status: Optional[str] = None
    registration_link: Optional[str] = None
    category: Optional[str] = None
    thumbnail_url: Optional[str] = None
    source_lang: Optional[str] = "fr"

class Event(EventBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
