from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict

class LiveStatBase(BaseModel):
    label: Dict[str, str]
    value: str
    icon_name: Optional[str] = None
    category: Optional[str] = None

class LiveStatCreate(LiveStatBase):
    pass

class LiveStatUpdate(LiveStatBase):
    value: Optional[str] = None

class LiveStat(LiveStatBase):
    id: int
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
