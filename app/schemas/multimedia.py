import json
from pydantic import BaseModel, ConfigDict, field_validator, ValidationInfo
from datetime import datetime
from typing import Optional, Dict, Any

class MultimediaBase(BaseModel):
    title: Dict[str, str]
    media_url: str
    thumbnail_url: Optional[str] = None
    type: Optional[str] = None # photo, video
    category: Optional[Dict[str, str]] = None # {"en": "Nature", "fr": "Nature"}
    album_id: Optional[int] = None

    @field_validator("*", mode="before")
    @classmethod
    def empty_string_to_none(cls, v: Any, info: ValidationInfo) -> Any:
        if info.field_name == "source_lang":
            return v
        if isinstance(v, str) and not v.strip():
            return None
        return v

    @field_validator("title", "category", mode="before")
    @classmethod
    def parse_legacy_json_or_string(cls, value: Any) -> Optional[Dict[str, str]]:
        if isinstance(value, str):
            try:
                # Try parsing if it's a JSON string
                parsed = json.loads(value)
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                pass
            
            # If it's a plain string
            return {"en": value, "fr": value}
        return value

class MultimediaCreate(BaseModel):
    title: Any
    media_url: str
    thumbnail_url: Optional[str] = None
    type: Optional[str] = None
    category: Optional[Any] = None
    album_id: Optional[int] = None
    source_lang: str = "fr"

class MultimediaUpdate(BaseModel):
    title: Optional[Any] = None
    media_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    type: Optional[str] = None
    category: Optional[Any] = None
    album_id: Optional[int] = None
    source_lang: Optional[str] = None

class Multimedia(MultimediaBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
