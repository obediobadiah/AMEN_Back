import json
from pydantic import BaseModel, ConfigDict, field_validator, ValidationInfo
from datetime import datetime
from typing import Optional, Dict, Any

class LiveStatBase(BaseModel):
    label: Dict[str, str]
    value: str
    icon_name: Optional[str] = None
    category: Optional[str] = None

    @field_validator("*", mode="before")
    @classmethod
    def empty_string_to_none(cls, v: Any, info: ValidationInfo) -> Any:
        if isinstance(v, str) and not v.strip():
            return None
        return v

    @field_validator("label", mode="before")
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

class LiveStatCreate(BaseModel):
    label: Any
    value: str
    icon_name: Optional[str] = None
    category: Optional[str] = None

class LiveStatUpdate(BaseModel):
    label: Optional[Any] = None
    value: Optional[str] = None
    icon_name: Optional[str] = None
    category: Optional[str] = None

class LiveStat(LiveStatBase):
    id: int
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
