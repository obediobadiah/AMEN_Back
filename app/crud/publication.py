from sqlalchemy.orm import Session
from ..models.all_models import Publication
from ..schemas.publication import PublicationCreate, PublicationUpdate
from ..core.translate import multi_translate

def get_publications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Publication).order_by(Publication.date.desc()).offset(skip).limit(limit).all()

def get_publication_by_id(db: Session, publication_id: int):
    return db.query(Publication).filter(Publication.id == publication_id).first()

CATEGORY_MAP = {
    "annual": {"en": "Annual Report", "fr": "Rapport Annuel"},
    "technical": {"en": "Technical Guide", "fr": "Guide Technique"},
    "research": {"en": "Research Paper", "fr": "Document de Recherche"}
}

def create_publication(db: Session, publication: PublicationCreate):
    pub_data = publication.model_dump()
    source_lang = pub_data.pop("source_lang", "fr")
    
    # Auto-translate bilingual fields
    pub_data["title"] = multi_translate(pub_data["title"], source_lang)
    if pub_data.get("description"):
        pub_data["description"] = multi_translate(pub_data["description"], source_lang)
    
    # Handle category mapping
    if pub_data.get("category"):
        pub_data["category"] = CATEGORY_MAP.get(pub_data["category"], {"en": pub_data["category"], "fr": pub_data["category"]})
    
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
    source_lang = update_data.pop("source_lang", "fr")
    
    # Handle re-translation if flat strings are provided
    if isinstance(update_data.get("title"), str):
        update_data["title"] = multi_translate(update_data["title"], source_lang)
    if isinstance(update_data.get("description"), str):
        update_data["description"] = multi_translate(update_data["description"], source_lang)
    if isinstance(update_data.get("category"), str):
        update_data["category"] = CATEGORY_MAP.get(update_data["category"], {"en": update_data["category"], "fr": update_data["category"]})
        
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
