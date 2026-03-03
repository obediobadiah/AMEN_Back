from sqlalchemy.orm import Session
from ..models.all_models import Inquiry
from ..schemas.inquiry import InquiryCreate, InquiryUpdate

def get_inquiries(db: Session, skip: int = 0, limit: int = 100, type: str = None):
    query = db.query(Inquiry)
    if type:
        query = query.filter(Inquiry.type == type)
    return query.order_by(Inquiry.created_at.desc()).offset(skip).limit(limit).all()

def create_inquiry(db: Session, inquiry: InquiryCreate):
    db_inquiry = Inquiry(**inquiry.model_dump())
    db.add(db_inquiry)
    db.commit()
    db.refresh(db_inquiry)
    return db_inquiry

def update_inquiry(db: Session, inquiry_id: int, inquiry_update: InquiryUpdate):
    db_inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not db_inquiry:
        return None
    
    update_data = inquiry_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_inquiry, field, value)
    
    db.commit()
    db.refresh(db_inquiry)
    return db_inquiry

def delete_inquiry(db: Session, inquiry_id: int):
    db_inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not db_inquiry:
        return None
    db.delete(db_inquiry)
    db.commit()
    return db_inquiry
