import json
from pydantic import BaseModel, ConfigDict, field_validator, ValidationInfo
from datetime import datetime
from typing import Optional, Dict, List, Any

class LocalizedString(BaseModel):
    en: str
    fr: str

class NewsBase(BaseModel):
    title: Dict[str, str]
    content: Dict[str, str]
    excerpt: Optional[Dict[str, str]] = None
    author: Optional[str] = None
    category: Optional[Dict[str, str]] = None
    status: Optional[Dict[str, str]] = None
    reading_time: Optional[int] = None
    thumbnail_url: Optional[str] = None
    tags: Optional[List[str]] = None

    @field_validator("*", mode="before")
    @classmethod
    def empty_string_to_none(cls, v: Any, info: ValidationInfo) -> Any:
        if info.field_name == "source_lang":
            return v
        if isinstance(v, str) and not v.strip():
            return None
        return v

    @field_validator("category", "status", mode="before")
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
            
            # If it's a plain string like "Published" or "impact"
            return {"en": value, "fr": value}
        return value

class NewsCreate(BaseModel):
    title: Any
    content: Any
    excerpt: Optional[Any] = None
    author: Optional[str] = None
    category: Optional[Any] = None
    status: Optional[Any] = "Draft"
    reading_time: Optional[int] = None
    thumbnail_url: Optional[str] = None
    tags: Optional[List[str]] = None
    source_lang: str = "fr" # Default to French, or "en" based on admin input

class NewsUpdate(BaseModel):
    title: Optional[Any] = None
    content: Optional[Any] = None
    excerpt: Optional[Any] = None
    status: Optional[Any] = None
    category: Optional[Any] = None
    author: Optional[str] = None
    reading_time: Optional[int] = None
    thumbnail_url: Optional[str] = None
    source_lang: Optional[str] = None
    published_date: Optional[datetime] = None

class News(NewsBase):
    id: int
    published_date: datetime
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
