import json
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional, Dict, Any

class GovernanceBase(BaseModel):
    name: str
    role: Dict[str, str]
    bio: Optional[Dict[str, str]] = None
    photo_url: Optional[str] = None
    organ_id: Optional[str] = None # ag, cd, pe, dg
    order: Optional[int] = 0

    @field_validator("role", "bio", mode="before")
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

class GovernanceCreate(GovernanceBase):
    pass

class GovernanceUpdate(GovernanceBase):
    name: Optional[str] = None

class Governance(GovernanceBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
