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

router = APIRouter()


@router.post("/upload")
async def upload_resource_file(file: UploadFile = File(...)):
    """
    Upload a resource file (PDF, DOCX, XLS, etc.).
    For PDFs, automatically generates a thumbnail from the first page.
    """
    static_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
        "static"
    )
    docs_dir = os.path.join(static_dir, "documents")
    images_dir = os.path.join(static_dir, "images")

    os.makedirs(docs_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    file_extension = os.path.splitext(file.filename)[1].lower()
    base_name = str(uuid.uuid4())
    filename = f"{base_name}{file_extension}"
    file_path = os.path.join(docs_dir, filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size_bytes = os.path.getsize(file_path)
    file_size = f"{file_size_bytes / (1024 * 1024):.1f} MB"

    thumbnail_url = None
    file_type = file_extension.replace(".", "").upper()

    # Generate thumbnail from first page if it's a PDF
    if file_type == "PDF":
        try:
            pdf_doc = fitz.open(file_path)
            if len(pdf_doc) > 0:
                first_page = pdf_doc.load_page(0)
                pix = first_page.get_pixmap(dpi=150)
                thumb_filename = f"{base_name}_thumb.jpg"
                thumb_path = os.path.join(images_dir, thumb_filename)
                pix.save(thumb_path)
                thumbnail_url = f"/static/images/{thumb_filename}"
            pdf_doc.close()
        except Exception as e:
            print(f"Error generating resource thumbnail: {e}")

    return {
        "file_url": f"/static/documents/{filename}",
        "thumbnail_url": thumbnail_url,
        "file_size": file_size,
        "file_type": file_type,
    }


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
