from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ....crud import album as crud_album
from ....schemas import album as schema_album
from ....db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[schema_album.Album])
def read_albums(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_album.get_albums(db, skip=skip, limit=limit)

@router.get("/{album_id}", response_model=schema_album.Album)
def read_single_album(album_id: int, db: Session = Depends(get_db)):
    db_album = crud_album.get_album_by_id(db, album_id)
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return db_album

@router.post("/", response_model=schema_album.Album)
def create_album(album: schema_album.AlbumCreate, db: Session = Depends(get_db)):
    return crud_album.create_album(db, album)

@router.put("/{album_id}", response_model=schema_album.Album)
def update_album(album_id: int, album: schema_album.AlbumUpdate, db: Session = Depends(get_db)):
    db_album = crud_album.update_album(db, album_id, album)
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return db_album

@router.delete("/{album_id}")
def delete_album(album_id: int, db: Session = Depends(get_db)):
    db_album = crud_album.delete_album(db, album_id)
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return {"message": "Album deleted"}
