import json
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional, Dict, Any

class AlbumBase(BaseModel):
    name: Dict[str, str]
    description: Optional[Dict[str, str]] = None
    thumbnail_url: Optional[str] = None
    is_public: bool = False

    @field_validator("name", "description", mode="before")
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

class AlbumCreate(BaseModel):
    name: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    is_public: bool = False
    source_lang: str = "fr"

class AlbumUpdate(BaseModel):
    name: Optional[Dict[str, str] | str] = None
    description: Optional[Dict[str, str] | str] = None
    thumbnail_url: Optional[str] = None
    is_public: Optional[bool] = None
    source_lang: Optional[str] = "fr"

class Album(AlbumBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
