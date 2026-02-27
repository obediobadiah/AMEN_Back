import json
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional, Dict, List, Any

class ProjectBase(BaseModel):
    title: Dict[str, str]
    description: Optional[Dict[str, str]] = None
    status: Optional[str] = None # Active, Completed, Upcoming
    location: Optional[Dict[str, str]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    category: Optional[str] = None
    impact_stats: Optional[Dict[str, Dict[str, str]]] = None # {"en": {"label": "Trees", "value": "100"}, ...}
    overview: Optional[Dict[str, str]] = None
    goals: Optional[Dict[str, List[str]]] = None
    achievements: Optional[Dict[str, List[str]]] = None
    image_url: Optional[str] = None

    @field_validator("title", "description", "location", "overview", mode="before")
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

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    title: Optional[Dict[str, str]] = None

class Project(ProjectBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
