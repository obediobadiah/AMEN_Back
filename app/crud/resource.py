from sqlalchemy.orm import Session
from ..models.all_models import Resource
from ..schemas.resource import ResourceCreate, ResourceUpdate
from ..core.translate import multi_translate

def get_resources(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Resource).offset(skip).limit(limit).all()

def get_resource_by_id(db: Session, resource_id: int):
    return db.query(Resource).filter(Resource.id == resource_id).first()

def create_resource(db: Session, resource: ResourceCreate):
    resource_data = resource.model_dump()
    
    # Auto-translate
    resource_data["title"] = multi_translate(resource_data["title"])
    if resource_data.get("description"):
        resource_data["description"] = multi_translate(resource_data["description"])
        
    db_resource = Resource(**resource_data)
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def update_resource(db: Session, resource_id: int, resource: ResourceUpdate):
    db_resource = get_resource_by_id(db, resource_id)
    if not db_resource:
        return None
        
    update_data = resource.model_dump(exclude_unset=True)
    
    # Handle re-translation
    if isinstance(update_data.get("title"), str):
        update_data["title"] = multi_translate(update_data["title"])
    if isinstance(update_data.get("description"), str):
        update_data["description"] = multi_translate(update_data["description"])
        
    for key, value in update_data.items():
        setattr(db_resource, key, value)
        
    db.commit()
    db.refresh(db_resource)
    return db_resource

def delete_resource(db: Session, resource_id: int):
    db_resource = get_resource_by_id(db, resource_id)
    if not db_resource:
        return None
    db.delete(db_resource)
    db.commit()
    return db_resource
