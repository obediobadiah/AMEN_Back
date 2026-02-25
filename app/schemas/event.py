from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Union

class EventBase(BaseModel):
    title: Dict[str, str]
    description: Optional[Dict[str, str]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[Dict[str, str]] = None
    status: Optional[str] = None # Upcoming, Past
    registration_link: Optional[str] = None
    category: Optional[str] = None
    thumbnail_url: Optional[str] = None

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    status: Optional[str] = None
    registration_link: Optional[str] = None
    category: Optional[str] = None
    thumbnail_url: Optional[str] = None
    source_lang: Optional[str] = "fr"

class EventUpdate(BaseModel):
    title: Optional[Union[str, Dict[str, str]]] = None
    description: Optional[Union[str, Dict[str, str]]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[Union[str, Dict[str, str]]] = None
    status: Optional[str] = None
    registration_link: Optional[str] = None
    category: Optional[str] = None
    thumbnail_url: Optional[str] = None
    source_lang: Optional[str] = "fr"

class Event(EventBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
