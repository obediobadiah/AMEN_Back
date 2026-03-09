from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from ....crud import publication as crud_publication
from ....schemas import publication as schema_publication
from ....db.session import get_db
import os
import uuid
import shutil
import fitz # PyMuPDF
from ....core.supabase import upload_file_to_supabase, supabase_client

router = APIRouter()

@router.post("/upload")
async def upload_publication(file: UploadFile = File(...)):
    file_extension = os.path.splitext(file.filename)[1].lower()
    base_name = str(uuid.uuid4())
    filename = f"{base_name}{file_extension}"
    
    # Save to tmp for Vercel support
    tmp_path = os.path.join("/tmp", filename)
    thumb_tmp_path = os.path.join("/tmp", f"{base_name}_thumb.jpg")
    thumb_filename = f"{base_name}_thumb.jpg"
    
    thumbnail_url = None
    file_url = None
    
    try:
        # Save uploaded file temporarily
        with open(tmp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        file_size_bytes = os.path.getsize(tmp_path)
        file_size = f"{file_size_bytes / (1024 * 1024):.1f} MB".replace(".0 MB", " MB")
        file_type = file_extension.replace(".", "").upper()
        
        # Generate thumbnail if it's a PDF
        if file_type == "PDF":
            try:
                pdf_doc = fitz.open(tmp_path)
                if len(pdf_doc) > 0:
                    first_page = pdf_doc.load_page(0)
                    pix = first_page.get_pixmap(dpi=150)
                    pix.save(thumb_tmp_path)
                pdf_doc.close()
            except Exception as e:
                print(f"Error generating thumbnail: {e}")
        
        content_type = file.content_type
        
        if supabase_client:
            # Upload main file to Supabase
            file_url = upload_file_to_supabase("documents", tmp_path, filename, content_type)
            # Upload thumbnail if exists
            if os.path.exists(thumb_tmp_path):
                thumbnail_url = upload_file_to_supabase("images", thumb_tmp_path, thumb_filename, "image/jpeg")
        else:
            # Local fallback
            static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "static")
            docs_dir = os.path.join(static_dir, "documents")
            images_dir = os.path.join(static_dir, "images")
            os.makedirs(docs_dir, exist_ok=True)
            os.makedirs(images_dir, exist_ok=True)
            
            local_path = os.path.join(docs_dir, filename)
            shutil.copy(tmp_path, local_path)
            file_url = f"/static/documents/{filename}"
            
            if os.path.exists(thumb_tmp_path):
                thumb_local_path = os.path.join(images_dir, thumb_filename)
                shutil.copy(thumb_tmp_path, thumb_local_path)
                thumbnail_url = f"/static/images/{thumb_filename}"
                
        return {
            "file_url": file_url,
            "thumbnail_url": thumbnail_url,
            "file_size": file_size,
            "file_type": file_type
        }
    finally:
        # Clean up tmp files
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        if os.path.exists(thumb_tmp_path):
            os.remove(thumb_tmp_path)

@router.get("/", response_model=List[schema_publication.Publication])
def read_publications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_publication.get_publications(db, skip=skip, limit=limit)

@router.get("/{publication_id}", response_model=schema_publication.Publication)
def read_single_publication(publication_id: int, db: Session = Depends(get_db)):
    db_publication = crud_publication.get_publication_by_id(db, publication_id)
    if db_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")
    return db_publication

@router.post("/", response_model=schema_publication.Publication)
def create_publication(publication: schema_publication.PublicationCreate, db: Session = Depends(get_db)):
    return crud_publication.create_publication(db, publication)

@router.put("/{publication_id}", response_model=schema_publication.Publication)
def update_publication(publication_id: int, publication: schema_publication.PublicationUpdate, db: Session = Depends(get_db)):
    db_publication = crud_publication.update_publication(db, publication_id, publication)
    if db_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")
    return db_publication

@router.delete("/{publication_id}")
def delete_publication(publication_id: int, db: Session = Depends(get_db)):
    db_publication = crud_publication.delete_publication(db, publication_id)
    if db_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")
    return {"message": "Publication deleted"}

@router.post("/{publication_id}/download")
def record_download(publication_id: int, db: Session = Depends(get_db)):
    db_publication = crud_publication.get_publication_by_id(db, publication_id)
    if db_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")
    db_publication.downloads = (db_publication.downloads or 0) + 1
    db.commit()
    db.refresh(db_publication)
    return {"message": "Download recorded", "downloads": db_publication.downloads}
