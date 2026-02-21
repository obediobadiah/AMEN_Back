from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....crud import event as crud_event
from ....schemas import event as schema_event
from ....db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[schema_event.Event])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_event.get_events(db, skip=skip, limit=limit)

@router.get("/{event_id}", response_model=schema_event.Event)
def read_single_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud_event.get_event_by_id(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@router.post("/", response_model=schema_event.Event)
def create_event(event: schema_event.EventCreate, db: Session = Depends(get_db)):
    return crud_event.create_event(db, event)

@router.put("/{event_id}", response_model=schema_event.Event)
def update_event(event_id: int, event: schema_event.EventUpdate, db: Session = Depends(get_db)):
    db_event = crud_event.update_event(db, event_id, event)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud_event.delete_event(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted"}
