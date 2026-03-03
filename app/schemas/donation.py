from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class DonationBase(BaseModel):
    donor: Optional[str] = None
    email: Optional[EmailStr] = None
    amount: int
    currency: str = "USD"
    frequency: str # oneTime, monthly
    method: str # card, mobile, bank
    status: str = "completed"

class DonationCreate(DonationBase):
    pass

class DonationUpdate(BaseModel):
    donor: Optional[str] = None
    email: Optional[EmailStr] = None
    amount: Optional[int] = None
    currency: Optional[str] = None
    frequency: Optional[str] = None
    method: Optional[str] = None
    status: Optional[str] = None

class Donation(DonationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
