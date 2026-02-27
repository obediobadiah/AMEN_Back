from sqlalchemy.orm import Session
from ..models.all_models import Album
from ..schemas.album import AlbumCreate, AlbumUpdate
from ..core.translate import multi_translate

def get_albums(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Album).order_by(Album.id.desc()).offset(skip).limit(limit).all()

def get_album_by_id(db: Session, album_id: int):
    return db.query(Album).filter(Album.id == album_id).first()

def create_album(db: Session, album: AlbumCreate):
    album_data = album.model_dump()
    source_lang = album_data.pop("source_lang", "fr")
    
    # Auto-translate
    album_data["name"] = multi_translate(album_data["name"], source_lang)
    if album_data.get("description"):
        album_data["description"] = multi_translate(album_data["description"], source_lang)
    
    db_album = Album(**album_data)
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album

def update_album(db: Session, album_id: int, album: AlbumUpdate):
    db_album = get_album_by_id(db, album_id)
    if not db_album:
        return None
    
    update_data = album.model_dump(exclude_unset=True)
    source_lang = update_data.pop("source_lang", "fr")
    
    # Handle re-translation
    if isinstance(update_data.get("name"), str):
        update_data["name"] = multi_translate(update_data["name"], source_lang)
    if isinstance(update_data.get("description"), str):
        update_data["description"] = multi_translate(update_data["description"], source_lang)
        
    for key, value in update_data.items():
        setattr(db_album, key, value)
        
    db.commit()
    db.refresh(db_album)
    return db_album

def delete_album(db: Session, album_id: int):
    db_album = get_album_by_id(db, album_id)
    if not db_album:
        return None
    db.delete(db_album)
    db.commit()
    return db_album
