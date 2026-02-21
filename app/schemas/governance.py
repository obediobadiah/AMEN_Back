from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict

class GovernanceBase(BaseModel):
    name: str
    role: Dict[str, str]
    bio: Optional[Dict[str, str]] = None
    photo_url: Optional[str] = None
    organ_id: Optional[str] = None # ag, cd, pe, dg
    order: Optional[int] = 0

class GovernanceCreate(GovernanceBase):
    pass

class GovernanceUpdate(GovernanceBase):
    name: Optional[str] = None

class Governance(GovernanceBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
