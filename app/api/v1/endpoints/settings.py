from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....crud import settings as crud_settings
from ....schemas.settings import PortalSettingsOut, PortalSettingsUpdate
from ....db.session import get_db
from ....core.security import get_current_user, require_admin
from ....models.all_models import PortalUser

router = APIRouter()


@router.get("/", response_model=PortalSettingsOut)
def read_settings(
    db: Session = Depends(get_db),
    current_user: PortalUser = Depends(get_current_user),
):
    """Any authenticated user can read settings."""
    return crud_settings.get_settings(db)


@router.put("/", response_model=PortalSettingsOut)
def update_settings(
    settings_in: PortalSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: PortalUser = Depends(require_admin),
):
    """Only admins can update settings."""
    return crud_settings.update_settings(db, settings_in, updated_by=current_user.id)
