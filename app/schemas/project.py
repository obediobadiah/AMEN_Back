import json
from pydantic import BaseModel, ConfigDict, field_validator, ValidationInfo
from datetime import datetime
from typing import Optional, Dict, List, Any

class ProjectBase(BaseModel):
    title: Any # Can be Dict[str, str] or str
    description: Optional[Any] = None
    status: Optional[str] = None # Active, Completed, Upcoming
    location: Optional[Any] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    category: Optional[Any] = None
    impact_stats: Optional[Any] = None 
    overview: Optional[Any] = None
    goals: Optional[Any] = None
    achievements: Optional[Any] = None
    image_url: Optional[str] = None

    @field_validator("*", mode="before")
    @classmethod
    def empty_string_to_none(cls, v: Any, info: ValidationInfo) -> Any:
        if info.field_name == "source_lang": # Don't touch source_lang
            return v
        if isinstance(v, str) and not v.strip():
            return None
        return v

class ProjectCreate(ProjectBase):
    source_lang: Optional[str] = "fr"

class ProjectUpdate(ProjectBase):
    title: Optional[Any] = None
    source_lang: Optional[str] = "fr"

    @field_validator("title", "description", "location", "category", "impact_stats", "overview", mode="before")
    @classmethod
    def parse_legacy_json_or_string(cls, value: Any) -> Any:
        if isinstance(value, str) and value:
            try:
                # Try parsing if it's a JSON string
                parsed = json.loads(value)
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                pass
            
            # If it's a plain string, keep it as string for Create/Update schemas
            # The Project schema will then convert it if needed
        return value

class Project(ProjectBase):
    id: int
    title: Dict[str, str]
    description: Optional[Dict[str, str]] = None
    location: Optional[Dict[str, str]] = None
    category: Optional[Dict[str, str]] = None
    impact_stats: Optional[Dict[str, Any]] = None
    overview: Optional[Dict[str, str]] = None
    goals: Optional[Dict[str, List[str]]] = None
    achievements: Optional[Dict[str, List[str]]] = None
    created_at: datetime
    
    @field_validator("title", "description", "location", "category", "impact_stats", "overview", mode="before")
    @classmethod
    def ensure_dict(cls, value: Any) -> Optional[Dict[str, str]]:
        if isinstance(value, str) and value:
            try:
                parsed = json.loads(value)
                if isinstance(parsed, dict):
                    return parsed
            except:
                pass
            return {"en": value, "fr": value}
        return value

    @field_validator("goals", "achievements", mode="before")
    @classmethod
    def ensure_list_dict(cls, value: Any) -> Optional[Dict[str, List[str]]]:
        if isinstance(value, str) and value:
            try:
                parsed = json.loads(value)
                if isinstance(parsed, dict):
                    return parsed
            except:
                pass
            return {"en": [value], "fr": [value]}
        return value

    model_config = ConfigDict(from_attributes=True)
