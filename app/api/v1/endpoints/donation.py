from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....db.session import get_db
from ....crud import donation as crud_donation
from ....schemas import donation as schema_donation

router = APIRouter()

@router.get("/", response_model=List[schema_donation.Donation])
def read_donations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_donation.get_donations(db, skip=skip, limit=limit)

@router.get("/{id}", response_model=schema_donation.Donation)
def read_donation(id: int, db: Session = Depends(get_db)):
    db_donation = crud_donation.get_donation(db, donation_id=id)
    if db_donation is None:
        raise HTTPException(status_code=404, detail="Donation not found")
    return db_donation

@router.post("/", response_model=schema_donation.Donation)
def create_donation(donation: schema_donation.DonationCreate, db: Session = Depends(get_db)):
    return crud_donation.create_donation(db=db, donation=donation)

@router.put("/{id}", response_model=schema_donation.Donation)
def update_donation(id: int, donation: schema_donation.DonationUpdate, db: Session = Depends(get_db)):
    db_donation = crud_donation.update_donation(db, donation_id=id, donation=donation)
    if db_donation is None:
        raise HTTPException(status_code=404, detail="Donation not found")
    return db_donation

@router.delete("/{id}")
def delete_donation(id: int, db: Session = Depends(get_db)):
    success = crud_donation.delete_donation(db, donation_id=id)
    if not success:
        raise HTTPException(status_code=404, detail="Donation not found")
    return {"status": "success"}
