from sqlalchemy.orm import Session
from ..models.all_models import Multimedia
from ..schemas.multimedia import MultimediaCreate, MultimediaUpdate
from ..core.translate import multi_translate

def get_multimedia(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Multimedia).order_by(Multimedia.id.desc()).offset(skip).limit(limit).all()

def get_multimedia_by_id(db: Session, multimedia_id: int):
    return db.query(Multimedia).filter(Multimedia.id == multimedia_id).first()

def create_multimedia(db: Session, multimedia: MultimediaCreate):
    media_data = multimedia.model_dump()
    media_data.pop("source_lang", None)
    
    # Auto-translate
    media_data["title"] = multi_translate(media_data["title"])
    if media_data.get("category"):
        media_data["category"] = multi_translate(media_data["category"])
    
    db_multimedia = Multimedia(**media_data)
    db.add(db_multimedia)
    db.commit()
    db.refresh(db_multimedia)
    return db_multimedia

def update_multimedia(db: Session, multimedia_id: int, multimedia: MultimediaUpdate):
    db_multimedia = get_multimedia_by_id(db, multimedia_id)
    if not db_multimedia:
        return None
    
    update_data = multimedia.model_dump(exclude_unset=True)
    update_data.pop("source_lang", None)
    
    # Handle re-translation if flat strings are provided
    if isinstance(update_data.get("title"), str):
        update_data["title"] = multi_translate(update_data["title"])
    if isinstance(update_data.get("category"), str):
        update_data["category"] = multi_translate(update_data["category"])
        
    for key, value in update_data.items():
        setattr(db_multimedia, key, value)
        
    db.commit()
    db.refresh(db_multimedia)
    return db_multimedia

def delete_multimedia(db: Session, multimedia_id: int):
    db_multimedia = get_multimedia_by_id(db, multimedia_id)
    if not db_multimedia:
        return None
    db.delete(db_multimedia)
    db.commit()
    return db_multimedia
