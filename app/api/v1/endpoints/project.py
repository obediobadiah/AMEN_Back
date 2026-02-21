from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....crud import project as crud_project
from ....schemas import project as schema_project
from ....db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[schema_project.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_project.get_projects(db, skip=skip, limit=limit)

@router.get("/{project_id}", response_model=schema_project.Project)
def read_single_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud_project.get_project_by_id(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.post("/", response_model=schema_project.Project)
def create_project(project: schema_project.ProjectCreate, db: Session = Depends(get_db)):
    return crud_project.create_project(db, project)

@router.put("/{project_id}", response_model=schema_project.Project)
def update_project(project_id: int, project: schema_project.ProjectUpdate, db: Session = Depends(get_db)):
    db_project = crud_project.update_project(db, project_id, project)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud_project.delete_project(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted"}
