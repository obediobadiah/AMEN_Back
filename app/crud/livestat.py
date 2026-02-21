from sqlalchemy.orm import Session
from ..models.all_models import LiveStat
from ..schemas.livestat import LiveStatCreate, LiveStatUpdate

def get_stats(db: Session, category: str = None):
    query = db.query(LiveStat)
    if category:
        query = query.filter(LiveStat.category == category)
    return query.all()

def create_stat(db: Session, stat: LiveStatCreate):
    db_stat = LiveStat(**stat.model_dump())
    db.add(db_stat)
    db.commit()
    db.refresh(db_stat)
    return db_stat

def update_stat(db: Session, stat_id: int, stat: LiveStatUpdate):
    db_stat = db.query(LiveStat).filter(LiveStat.id == stat_id).first()
    if not db_stat:
        return None
    for key, value in stat.model_dump(exclude_unset=True).items():
        setattr(db_stat, key, value)
    db.commit()
    db.refresh(db_stat)
    return db_stat
