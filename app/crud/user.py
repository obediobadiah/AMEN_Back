from datetime import datetime, timezone
from sqlalchemy.orm import Session
from typing import List, Optional

from ..models.all_models import PortalUser
from ..schemas.user import UserCreate, UserUpdate
from ..core.security import hash_password, verify_password


def get_user_by_email(db: Session, email: str) -> Optional[PortalUser]:
    return db.query(PortalUser).filter(PortalUser.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[PortalUser]:
    return db.query(PortalUser).filter(PortalUser.id == user_id).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[PortalUser]:
    return db.query(PortalUser).offset(skip).limit(limit).all()


def create_user(db: Session, user_in: UserCreate) -> PortalUser:
    db_user = PortalUser(
        name=user_in.name,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        role=user_in.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[PortalUser]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    # record last login
    user.last_login = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, user_in: UserUpdate) -> Optional[PortalUser]:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None

    update_data = user_in.model_dump(exclude_unset=True)

    # Hash the new password if provided
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> Optional[PortalUser]:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user


def ensure_default_admin(db: Session) -> None:
    """Create a default admin account if no admins exist."""
    admin_count = db.query(PortalUser).filter(PortalUser.role == "admin").count()
    if admin_count == 0:
        default_admin = PortalUser(
            name="Admin",
            email="admin@amen-ngo.org",
            hashed_password=hash_password("Admin@2024!"),
            role="admin",
            is_active=True,
        )
        db.add(default_admin)
        db.commit()
