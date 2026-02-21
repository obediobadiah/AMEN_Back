from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ....crud import governance as crud_gov
from ....schemas import governance as schema_gov
from ....db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[schema_gov.Governance])
def read_members(organ_id: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_gov.get_members(db, skip=skip, limit=limit, organ_id=organ_id)

@router.get("/{member_id}", response_model=schema_gov.Governance)
def read_single_member(member_id: int, db: Session = Depends(get_db)):
    db_member = crud_gov.get_member_by_id(db, member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member

@router.post("/", response_model=schema_gov.Governance)
def create_member(member: schema_gov.GovernanceCreate, db: Session = Depends(get_db)):
    return crud_gov.create_member(db, member)

@router.put("/{member_id}", response_model=schema_gov.Governance)
def update_member(member_id: int, member: schema_gov.GovernanceUpdate, db: Session = Depends(get_db)):
    db_member = crud_gov.update_member(db, member_id, member)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member

@router.delete("/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    db_member = crud_gov.delete_member(db, member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"message": "Member deleted"}
