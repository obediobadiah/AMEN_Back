from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ....crud import livestat as crud_stats
from ....schemas import livestat as schema_stats
from ....db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[schema_stats.LiveStat])
def read_stats(category: Optional[str] = None, db: Session = Depends(get_db)):
    return crud_stats.get_stats(db, category=category)

@router.post("/", response_model=schema_stats.LiveStat)
def create_stat(stat: schema_stats.LiveStatCreate, db: Session = Depends(get_db)):
    return crud_stats.create_stat(db, stat)

@router.put("/{stat_id}", response_model=schema_stats.LiveStat)
def update_stat(stat_id: int, stat: schema_stats.LiveStatUpdate, db: Session = Depends(get_db)):
    db_stat = crud_stats.update_stat(db, stat_id, stat)
    if db_stat is None:
        raise HTTPException(status_code=404, detail="Stat not found")
    return db_stat
