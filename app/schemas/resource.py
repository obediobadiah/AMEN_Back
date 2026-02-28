import json
from pydantic import BaseModel, ConfigDict, field_validator, ValidationInfo
from datetime import datetime
from typing import Optional, Dict, Any

class ResourceBase(BaseModel):
    title: Dict[str, str]
    description: Optional[Dict[str, str]] = None
    file_url: str
    file_size: Optional[str] = None
    file_type: Optional[str] = None # PDF, XLS
    category: Optional[str] = None # report, guide, infographic, policy, database
    publication_date: Optional[datetime] = None

    @field_validator("*", mode="before")
    @classmethod
    def empty_string_to_none(cls, v: Any, info: ValidationInfo) -> Any:
        if isinstance(v, str) and not v.strip():
            return None
        return v

    @field_validator("title", "description", mode="before")
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

class ResourceCreate(BaseModel):
    title: Any
    description: Optional[Any] = None
    file_url: str
    file_size: Optional[str] = None
    file_type: Optional[str] = None
    category: Optional[str] = None
    publication_date: Optional[datetime] = None

class ResourceUpdate(BaseModel):
    title: Optional[Any] = None
    description: Optional[Any] = None
    file_url: Optional[str] = None
    file_size: Optional[str] = None
    file_type: Optional[str] = None
    category: Optional[str] = None
    publication_date: Optional[datetime] = None

class Resource(ResourceBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
