import json
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional, Dict, Any

class LiveStatBase(BaseModel):
    label: Dict[str, str]
    value: str
    icon_name: Optional[str] = None
    category: Optional[str] = None

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

class LiveStatCreate(LiveStatBase):
    pass

class LiveStatUpdate(LiveStatBase):
    value: Optional[str] = None

class LiveStat(LiveStatBase):
    id: int
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
