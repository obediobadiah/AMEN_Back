from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....crud import resource as crud_resource
from ....schemas import resource as schema_resource
from ....db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[schema_resource.Resource])
def read_resources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_resource.get_resources(db, skip=skip, limit=limit)

@router.get("/{resource_id}", response_model=schema_resource.Resource)
def read_single_resource(resource_id: int, db: Session = Depends(get_db)):
    db_resource = crud_resource.get_resource_by_id(db, resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return db_resource

@router.post("/", response_model=schema_resource.Resource)
def create_resource(resource: schema_resource.ResourceCreate, db: Session = Depends(get_db)):
    return crud_resource.create_resource(db, resource)

@router.put("/{resource_id}", response_model=schema_resource.Resource)
def update_resource(resource_id: int, resource: schema_resource.ResourceUpdate, db: Session = Depends(get_db)):
    db_resource = crud_resource.update_resource(db, resource_id, resource)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return db_resource

@router.delete("/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    db_resource = crud_resource.delete_resource(db, resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return {"message": "Resource deleted"}
