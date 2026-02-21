from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict

class EventBase(BaseModel):
    title: Dict[str, str]
    description: Optional[Dict[str, str]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[Dict[str, str]] = None
    status: Optional[str] = None # Upcoming, Past
    registration_link: Optional[str] = None
    category: Optional[str] = None

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    title: Optional[Dict[str, str]] = None

class Event(EventBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
