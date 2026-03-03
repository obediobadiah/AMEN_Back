from sqlalchemy.orm import Session
from ..models.all_models import Donation
from ..schemas.donation import DonationCreate, DonationUpdate
from typing import List, Optional

def get_donations(db: Session, skip: int = 0, limit: int = 100) -> List[Donation]:
    return db.query(Donation).order_by(Donation.created_at.desc()).offset(skip).limit(limit).all()

def get_donation(db: Session, donation_id: int) -> Optional[Donation]:
    return db.query(Donation).filter(Donation.id == donation_id).first()

def create_donation(db: Session, donation: DonationCreate) -> Donation:
    db_donation = Donation(**donation.model_dump())
    db.add(db_donation)
    db.commit()
    db.refresh(db_donation)
    return db_donation

def update_donation(db: Session, donation_id: int, donation: DonationUpdate) -> Optional[Donation]:
    db_donation = get_donation(db, donation_id)
    if db_donation:
        for key, value in donation.model_dump(exclude_unset=True).items():
            setattr(db_donation, key, value)
        db.commit()
        db.refresh(db_donation)
    return db_donation

def delete_donation(db: Session, donation_id: int) -> bool:
    db_donation = get_donation(db, donation_id)
    if db_donation:
        db.delete(db_donation)
        db.commit()
        return True
    return False
