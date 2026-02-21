from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict, List

class LocalizedString(BaseModel):
    en: str
    fr: str

class NewsBase(BaseModel):
    title: Dict[str, str]
    content: Dict[str, str]
    excerpt: Optional[Dict[str, str]] = None
    author: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = "Draft"
    reading_time: Optional[int] = None
    thumbnail_url: Optional[str] = None
    tags: Optional[List[str]] = None

class NewsCreate(BaseModel):
    title: str
    content: str
    excerpt: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = "Draft"
    reading_time: Optional[int] = None
    thumbnail_url: Optional[str] = None
    tags: Optional[List[str]] = None
    source_lang: str = "fr" # Default to French, or "en" based on admin input

class NewsUpdate(BaseModel):
    title: Optional[Dict[str, str] | str] = None
    content: Optional[Dict[str, str] | str] = None
    excerpt: Optional[Dict[str, str] | str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None
    reading_time: Optional[int] = None
    thumbnail_url: Optional[str] = None
    source_lang: Optional[str] = None
    published_date: Optional[datetime] = None

class News(NewsBase):
    id: int
    published_date: datetime
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
