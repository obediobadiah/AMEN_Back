from sqlalchemy.orm import Session
from ..models.all_models import LiveStat
from ..schemas.livestat import LiveStatCreate, LiveStatUpdate
from ..core.translate import multi_translate

def get_stats(db: Session, category: str = None):
    query = db.query(LiveStat)
    if category:
        query = query.filter(LiveStat.category == category)
    return query.all()

def create_stat(db: Session, stat: LiveStatCreate):
    stat_data = stat.model_dump()
    
    # Auto-translate
    if isinstance(stat_data.get("label"), str):
        stat_data["label"] = multi_translate(stat_data["label"])
        
    db_stat = LiveStat(**stat_data)
    db.add(db_stat)
    db.commit()
    db.refresh(db_stat)
    return db_stat

def update_stat(db: Session, stat_id: int, stat: LiveStatUpdate):
    db_stat = db.query(LiveStat).filter(LiveStat.id == stat_id).first()
    if not db_stat:
        return None
        
    update_data = stat.model_dump(exclude_unset=True)
    
    # Handle re-translation
    if isinstance(update_data.get("label"), str):
        update_data["label"] = multi_translate(update_data["label"])
        
    for key, value in update_data.items():
        setattr(db_stat, key, value)
        
    db.commit()
    db.refresh(db_stat)
    return db_stat
