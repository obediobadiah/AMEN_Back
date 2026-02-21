from sqlalchemy.orm import Session
from ..models.all_models import Resource
from ..schemas.resource import ResourceCreate, ResourceUpdate

def get_resources(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Resource).offset(skip).limit(limit).all()

def get_resource_by_id(db: Session, resource_id: int):
    return db.query(Resource).filter(Resource.id == resource_id).first()

def create_resource(db: Session, resource: ResourceCreate):
    db_resource = Resource(**resource.model_dump())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def update_resource(db: Session, resource_id: int, resource: ResourceUpdate):
    db_resource = get_resource_by_id(db, resource_id)
    if not db_resource:
        return None
    for key, value in resource.model_dump(exclude_unset=True).items():
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
