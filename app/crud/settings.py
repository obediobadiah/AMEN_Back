from sqlalchemy.orm import Session
from typing import Optional

from ..models.all_models import PortalSettings
from ..schemas.settings import PortalSettingsUpdate


def get_settings(db: Session) -> PortalSettings:
    """Get the singleton settings row, creating it if it doesn't exist."""
    settings = db.query(PortalSettings).first()
    if not settings:
        settings = PortalSettings()
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


def update_settings(
    db: Session,
    settings_in: PortalSettingsUpdate,
    updated_by: Optional[int] = None,
) -> PortalSettings:
    settings = get_settings(db)
    update_data = settings_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(settings, field, value)
    if updated_by:
        settings.updated_by = updated_by
    db.commit()
    db.refresh(settings)
    return settings
