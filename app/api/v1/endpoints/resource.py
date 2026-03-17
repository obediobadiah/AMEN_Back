from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from ....crud import resource as crud_resource
from ....schemas import resource as schema_resource
from ....db.session import get_db
import os
import uuid
import shutil
import fitz  # PyMuPDF
from ....core.supabase import upload_file_to_supabase, supabase_client

router = APIRouter()


@router.post("/upload")
async def upload_resource_file(file: UploadFile = File(...)):
    """
    Upload a resource file (PDF, DOCX, XLS, etc.).
    For PDFs, automatically generates a thumbnail from the first page.
    """
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
        file_size = f"{file_size_bytes / (1024 * 1024):.1f} MB"
        file_type = file_extension.replace(".", "").upper()
        
        # Generate thumbnail from first page if it's a PDF
        if file_type == "PDF":
            try:
                pdf_doc = fitz.open(tmp_path)
                if len(pdf_doc) > 0:
                    first_page = pdf_doc.load_page(0)
                    pix = first_page.get_pixmap(dpi=150)
                    pix.save(thumb_tmp_path)
                pdf_doc.close()
            except Exception as e:
                print(f"Error generating resource thumbnail: {e}")
                
        content_type = file.content_type
        
        if supabase_client:
            # Upload main file to Supabase
            file_url = upload_file_to_supabase("documents", tmp_path, filename, content_type)
            # Upload thumbnail if exists
            if os.path.exists(thumb_tmp_path):
                thumbnail_url = upload_file_to_supabase("images", thumb_tmp_path, thumb_filename, "image/jpeg")
        else:
            # Local fallback
            try:
                static_dir = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                    "static"
                )
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
            except OSError:
                raise HTTPException(
                    status_code=500,
                    detail="File upload failed: Read-only file system. Please configure SUPABASE_URL and SUPABASE_KEY for production deployments."
                )

        return {
            "file_url": file_url,
            "thumbnail_url": thumbnail_url,
            "file_size": file_size,
            "file_type": file_type,
        }
    finally:
        # Clean up tmp files
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        if os.path.exists(thumb_tmp_path):
            os.remove(thumb_tmp_path)


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


@router.post("/{resource_id}/download")
def record_download(resource_id: int, db: Session = Depends(get_db)):
    """Increment the download counter for a resource."""
    db_resource = crud_resource.record_download(db, resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return {"message": "Download recorded", "downloads": db_resource.downloads}
