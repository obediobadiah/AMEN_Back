from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional, Dict

class InquiryBase(BaseModel):
    type: str # contact, volunteer, partner, newsletter
    name: Optional[str] = None
    email: EmailStr
    subject: Optional[str] = None
    message: Optional[str] = None
    data: Optional[Dict] = None # Extra info

class InquiryCreate(InquiryBase):
    pass

class Inquiry(InquiryBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
