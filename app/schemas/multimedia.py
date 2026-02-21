from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict

class MultimediaBase(BaseModel):
    title: Dict[str, str]
    media_url: str
    thumbnail_url: Optional[str] = None
    type: Optional[str] = None # photo, video
    category: Optional[str] = None # Nature, Health, Education

class MultimediaCreate(MultimediaBase):
    pass

class MultimediaUpdate(MultimediaBase):
    title: Optional[Dict[str, str]] = None
    media_url: Optional[str] = None

class Multimedia(MultimediaBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
