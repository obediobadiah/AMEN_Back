from sqlalchemy.orm import Session
from ..models.all_models import News
from ..schemas.news import NewsCreate, NewsUpdate

def get_news(db: Session, skip: int = 0, limit: int = 100):
    return db.query(News).offset(skip).limit(limit).all()

def get_news_by_id(db: Session, news_id: int):
    return db.query(News).filter(News.id == news_id).first()

from ..core.translate import multi_translate

def create_news(db: Session, news: NewsCreate):
    news_data = news.model_dump()
    source_lang = news_data.pop("source_lang", "fr")
    
    # Auto-translate bilingual fields
    news_data["title"] = multi_translate(news_data["title"], source_lang)
    news_data["content"] = multi_translate(news_data["content"], source_lang)
    if news_data.get("excerpt"):
        news_data["excerpt"] = multi_translate(news_data["excerpt"], source_lang)
    
    db_news = News(**news_data)
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

def update_news(db: Session, news_id: int, news: NewsUpdate):
    db_news = get_news_by_id(db, news_id)
    if not db_news:
        return None
    
    update_data = news.model_dump(exclude_unset=True)
    source_lang = update_data.pop("source_lang", "fr")
    
    # Handle re-translation if flat strings are provided
    if isinstance(update_data.get("title"), str):
        update_data["title"] = multi_translate(update_data["title"], source_lang)
    if isinstance(update_data.get("content"), str):
        update_data["content"] = multi_translate(update_data["content"], source_lang)
    if isinstance(update_data.get("excerpt"), str):
        update_data["excerpt"] = multi_translate(update_data["excerpt"], source_lang)
        
    for key, value in update_data.items():
        setattr(db_news, key, value)
        
    db.commit()
    db.refresh(db_news)
    return db_news

def delete_news(db: Session, news_id: int):
    db_news = get_news_by_id(db, news_id)
    if not db_news:
        return None
    db.delete(db_news)
    db.commit()
    return db_news
