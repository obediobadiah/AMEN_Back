from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....crud import multimedia as crud_multimedia
from ....schemas import multimedia as schema_multimedia
from ....db.session import get_db
import os
import uuid
import shutil
from fastapi import UploadFile, File

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Define upload path
    static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "static")
    images_dir = os.path.join(static_dir, "images")
    
    # Create unique filename
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(images_dir, filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Return URL (assuming local development default)
    # The frontend knows how to handle environment-specific base URLs
    return {"url": f"/static/images/{filename}"}

@router.get("/", response_model=List[schema_multimedia.Multimedia])
def read_multimedia(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_multimedia.get_multimedia(db, skip=skip, limit=limit)

@router.get("/{multimedia_id}", response_model=schema_multimedia.Multimedia)
def read_single_media(multimedia_id: int, db: Session = Depends(get_db)):
    db_multimedia = crud_multimedia.get_multimedia_by_id(db, multimedia_id)
    if db_multimedia is None:
        raise HTTPException(status_code=404, detail="Media not found")
    return db_multimedia

@router.post("/", response_model=schema_multimedia.Multimedia)
def create_media(multimedia: schema_multimedia.MultimediaCreate, db: Session = Depends(get_db)):
    return crud_multimedia.create_multimedia(db, multimedia)

@router.put("/{multimedia_id}", response_model=schema_multimedia.Multimedia)
def update_media(multimedia_id: int, multimedia: schema_multimedia.MultimediaUpdate, db: Session = Depends(get_db)):
    db_multimedia = crud_multimedia.update_multimedia(db, multimedia_id, multimedia)
    if db_multimedia is None:
        raise HTTPException(status_code=404, detail="Media not found")
    return db_multimedia

@router.delete("/{multimedia_id}")
def delete_media(multimedia_id: int, db: Session = Depends(get_db)):
    db_multimedia = crud_multimedia.delete_multimedia(db, multimedia_id)
    if db_multimedia is None:
        raise HTTPException(status_code=404, detail="Media not found")
    return {"message": "Media deleted"}
