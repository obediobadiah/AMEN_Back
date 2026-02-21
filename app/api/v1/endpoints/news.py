from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....crud import news as crud_news
from ....schemas import news as schema_news
from ....db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[schema_news.News])
def read_news(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_news.get_news(db, skip=skip, limit=limit)

@router.get("/{news_id}", response_model=schema_news.News)
def read_single_article(news_id: int, db: Session = Depends(get_db)):
    db_news = crud_news.get_news_by_id(db, news_id)
    if db_news is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_news

@router.post("/", response_model=schema_news.News)
def create_article(news: schema_news.NewsCreate, db: Session = Depends(get_db)):
    return crud_news.create_news(db, news)

@router.put("/{news_id}", response_model=schema_news.News)
def update_article(news_id: int, news: schema_news.NewsUpdate, db: Session = Depends(get_db)):
    db_news = crud_news.update_news(db, news_id, news)
    if db_news is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_news

@router.delete("/{news_id}")
def delete_article(news_id: int, db: Session = Depends(get_db)):
    db_news = crud_news.delete_news(db, news_id)
    if db_news is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"message": "Article deleted"}
