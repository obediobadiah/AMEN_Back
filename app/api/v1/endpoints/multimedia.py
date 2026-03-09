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
from ....core.supabase import upload_file_to_supabase, supabase_client

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Create unique filename
    file_extension = os.path.splitext(file.filename)[1].lower()
    filename = f"{uuid.uuid4()}{file_extension}"
    
    # Define temp upload path (writable on Vercel)
    tmp_path = os.path.join("/tmp", filename)
    
    try:
        # Save file temporarily
        with open(tmp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        content_type = file.content_type
        
        if supabase_client:
            # Upload to Supabase 'images' bucket
            bucket = "images" 
            file_url = upload_file_to_supabase(bucket, tmp_path, filename, content_type)
        else:
            # Fallback for local development if Supabase is not configured
            # Be aware that this won't persist on Vercel!
            static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "static")
            images_dir = os.path.join(static_dir, "images")
            os.makedirs(images_dir, exist_ok=True)
            local_path = os.path.join(images_dir, filename)
            shutil.copy(tmp_path, local_path)
            file_url = f"/static/images/{filename}"
            
        return {"url": file_url}
        
    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

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
