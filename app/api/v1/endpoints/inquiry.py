from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ....crud import inquiry as crud_inquiry
from ....schemas import inquiry as schema_inquiry
from ....db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[schema_inquiry.Inquiry])
def read_inquiries(type: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_inquiry.get_inquiries(db, skip=skip, limit=limit, type=type)

@router.post("/", response_model=schema_inquiry.Inquiry)
def create_inquiry(inquiry: schema_inquiry.InquiryCreate, db: Session = Depends(get_db)):
    return crud_inquiry.create_inquiry(db, inquiry)

@router.delete("/{inquiry_id}")
def delete_inquiry(inquiry_id: int, db: Session = Depends(get_db)):
    db_inquiry = crud_inquiry.delete_inquiry(db, inquiry_id)
    if db_inquiry is None:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return {"message": "Inquiry deleted"}
