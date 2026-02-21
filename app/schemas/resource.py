from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict

class ResourceBase(BaseModel):
    title: Dict[str, str]
    description: Optional[Dict[str, str]] = None
    file_url: str
    file_size: Optional[str] = None
    file_type: Optional[str] = None # PDF, XLS
    category: Optional[str] = None # report, guide, infographic, policy, database
    publication_date: Optional[datetime] = None

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(ResourceBase):
    title: Optional[Dict[str, str]] = None
    file_url: Optional[str] = None

class Resource(ResourceBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
