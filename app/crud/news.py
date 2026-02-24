from sqlalchemy.orm import Session
from ..models.all_models import News
from ..schemas.news import NewsCreate, NewsUpdate

def get_news(db: Session, skip: int = 0, limit: int = 100):
    return db.query(News).order_by(News.id.desc()).offset(skip).limit(limit).all()

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

    STATUS_MAP = {
        "Draft": {"en": "Draft", "fr": "Brouillon"},
        "Published": {"en": "Published", "fr": "Publié"},
        "Archived": {"en": "Archived", "fr": "Archivé"}
    }
    CATEGORY_MAP = {
        "impact": {"en": "Impact", "fr": "Impact"},
        "field": {"en": "Field", "fr": "Terrain"},
        "press": {"en": "Press", "fr": "Presse"}
    }

    if news_data.get("category"):
        news_data["category"] = CATEGORY_MAP.get(news_data["category"], {"en": news_data["category"], "fr": news_data["category"]})
    if news_data.get("status"):
        news_data["status"] = STATUS_MAP.get(news_data["status"], {"en": news_data["status"], "fr": news_data["status"]})
    
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
    
    STATUS_MAP = {
        "Draft": {"en": "Draft", "fr": "Brouillon"},
        "Published": {"en": "Published", "fr": "Publié"},
        "Archived": {"en": "Archived", "fr": "Archivé"}
    }
    CATEGORY_MAP = {
        "impact": {"en": "Impact", "fr": "Impact"},
        "field": {"en": "Field", "fr": "Terrain"},
        "press": {"en": "Press", "fr": "Presse"}
    }
    
    # Handle re-translation if flat strings are provided
    if isinstance(update_data.get("title"), str):
        update_data["title"] = multi_translate(update_data["title"], source_lang)
    if isinstance(update_data.get("content"), str):
        update_data["content"] = multi_translate(update_data["content"], source_lang)
    if isinstance(update_data.get("excerpt"), str):
        update_data["excerpt"] = multi_translate(update_data["excerpt"], source_lang)
    if isinstance(update_data.get("category"), str):
        update_data["category"] = CATEGORY_MAP.get(update_data["category"], {"en": update_data["category"], "fr": update_data["category"]})
    if isinstance(update_data.get("status"), str):
        update_data["status"] = STATUS_MAP.get(update_data["status"], {"en": update_data["status"], "fr": update_data["status"]})
        
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
