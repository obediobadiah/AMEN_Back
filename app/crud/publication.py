from sqlalchemy.orm import Session
from ..models.all_models import Publication
from ..schemas.publication import PublicationCreate, PublicationUpdate
from ..core.translate import multi_translate

def get_publications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Publication).order_by(Publication.date.desc()).offset(skip).limit(limit).all()

def get_publication_by_id(db: Session, publication_id: int):
    return db.query(Publication).filter(Publication.id == publication_id).first()

def create_publication(db: Session, publication: PublicationCreate):
    pub_data = publication.model_dump()
    pub_data.pop("source_lang", None)
    
    # Auto-translate bilingual fields
    pub_data["title"] = multi_translate(pub_data["title"])
    if pub_data.get("description"):
        pub_data["description"] = multi_translate(pub_data["description"])
    
    if isinstance(pub_data.get("category"), str):
        pub_data["category"] = multi_translate(pub_data["category"])
    
    db_publication = Publication(**pub_data)
    db.add(db_publication)
    db.commit()
    db.refresh(db_publication)
    return db_publication

def update_publication(db: Session, publication_id: int, publication: PublicationUpdate):
    db_publication = get_publication_by_id(db, publication_id)
    if not db_publication:
        return None
    
    update_data = publication.model_dump(exclude_unset=True)
    update_data.pop("source_lang", None)
    
    # Handle re-translation if flat strings are provided
    if isinstance(update_data.get("title"), str):
        update_data["title"] = multi_translate(update_data["title"])
    if isinstance(update_data.get("description"), str):
        update_data["description"] = multi_translate(update_data["description"])
    if isinstance(update_data.get("category"), str):
        update_data["category"] = multi_translate(update_data["category"])
        
    for key, value in update_data.items():
        setattr(db_publication, key, value)
        
    db.commit()
    db.refresh(db_publication)
    return db_publication

def delete_publication(db: Session, publication_id: int):
    db_publication = get_publication_by_id(db, publication_id)
    if not db_publication:
        return None
    db.delete(db_publication)
    db.commit()
    return db_publication
