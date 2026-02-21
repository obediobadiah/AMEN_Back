from sqlalchemy.orm import Session
from ..models.all_models import Multimedia
from ..schemas.multimedia import MultimediaCreate, MultimediaUpdate

def get_multimedia(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Multimedia).offset(skip).limit(limit).all()

def get_multimedia_by_id(db: Session, multimedia_id: int):
    return db.query(Multimedia).filter(Multimedia.id == multimedia_id).first()

def create_multimedia(db: Session, multimedia: MultimediaCreate):
    db_multimedia = Multimedia(**multimedia.model_dump())
    db.add(db_multimedia)
    db.commit()
    db.refresh(db_multimedia)
    return db_multimedia

def update_multimedia(db: Session, multimedia_id: int, multimedia: MultimediaUpdate):
    db_multimedia = get_multimedia_by_id(db, multimedia_id)
    if not db_multimedia:
        return None
    for key, value in multimedia.model_dump(exclude_unset=True).items():
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
