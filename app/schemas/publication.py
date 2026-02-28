from pydantic import BaseModel, ConfigDict, field_validator, ValidationInfo
from datetime import datetime
from typing import Optional, Dict, Any

class PublicationBase(BaseModel):
    title: Dict[str, str] | str
    description: Optional[Dict[str, str] | str] = None
    category: Optional[Dict[str, str] | str] = None
    date: Optional[datetime] = None
    file_url: str
    thumbnail_url: Optional[str] = None
    file_size: Optional[str] = None
    file_type: Optional[str] = None
    downloads: Optional[int] = 0

    @field_validator("*", mode="before")
    @classmethod
    def empty_string_to_none(cls, v: Any, info: ValidationInfo) -> Any:
        if info.field_name == "source_lang":
            return v
        if isinstance(v, str) and not v.strip():
            return None
        return v

    @field_validator("title", "description", "category", mode="before")
    @classmethod
    def ensure_dict(cls, value: Any) -> Any:
        if isinstance(value, str) and value:
            return {"en": value, "fr": value}
        return value

class PublicationCreate(BaseModel):
    title: Any
    description: Optional[Any] = None
    category: Optional[Any] = None
    date: Optional[datetime] = None
    file_url: str
    thumbnail_url: Optional[str] = None
    file_size: Optional[str] = None
    file_type: Optional[str] = None
    source_lang: str = "fr"

class PublicationUpdate(BaseModel):
    title: Optional[Any] = None
    description: Optional[Any] = None
    category: Optional[Any] = None
    date: Optional[datetime] = None
    file_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    source_lang: Optional[str] = None

class Publication(PublicationBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
