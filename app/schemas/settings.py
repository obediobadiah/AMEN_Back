from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional


class PortalSettingsUpdate(BaseModel):
    org_name: Optional[str] = None
    primary_email: Optional[str] = None
    website_url: Optional[str] = None
    two_factor_enabled: Optional[bool] = None
    activity_logging_enabled: Optional[bool] = None
    maintenance_mode: Optional[bool] = None


class PortalSettingsOut(BaseModel):
    id: int
    org_name: str
    primary_email: str
    website_url: str
    two_factor_enabled: bool
    activity_logging_enabled: bool
    maintenance_mode: bool
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
