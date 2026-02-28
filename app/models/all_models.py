from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from ..db.session import Base

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(JSONB, nullable=False) # {"en": "...", "fr": "..."}
    content = Column(JSONB, nullable=False) # {"en": "...", "fr": "..."}
    excerpt = Column(JSONB) # {"en": "...", "fr": "..."}
    author = Column(String)
    category = Column(JSONB) # {"en": "...", "fr": "..."}
    status = Column(JSONB, default={"en": "Draft", "fr": "Brouillon"}) # {"en": "...", "fr": "..."}
    reading_time = Column(Integer) # in minutes
    thumbnail_url = Column(String)
    tags = Column(JSONB) # ["tag1", "tag2"]
    published_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(JSONB, nullable=False)
    description = Column(JSONB)
    status = Column(String) # Active, Completed, Upcoming
    location = Column(JSONB) # {"en": "...", "fr": "..."}
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    category = Column(JSONB)
    impact_stats = Column(JSONB) # {"en": {"label": "...", "value": "..."}, "fr": {...}}
    overview = Column(JSONB)
    goals = Column(JSONB) # {"en": ["..."], "fr": ["..."]}
    achievements = Column(JSONB) # {"en": ["..."], "fr": ["..."]}
    image_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(JSONB, nullable=False)
    description = Column(JSONB)
    file_url = Column(String, nullable=False)
    file_size = Column(String)
    file_type = Column(String) # PDF, XLS
    category = Column(String) # report, guide, infographic, policy, database
    publication_date = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(JSONB, nullable=False)
    description = Column(JSONB)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    location = Column(JSONB)
    status = Column(String) # Upcoming, Past
    registration_link = Column(String)
    category = Column(String)
    thumbnail_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Publication(Base):
    __tablename__ = "publications"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(JSONB, nullable=False) # {"en": "...", "fr": "..."}
    description = Column(JSONB) # {"en": "...", "fr": "..."}
    category = Column(JSONB) # {"en": "...", "fr": "..."}
    date = Column(DateTime)
    file_url = Column(String, nullable=False)
    thumbnail_url = Column(String)
    file_size = Column(String)
    file_type = Column(String)
    downloads = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Album(Base):
    __tablename__ = "albums"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(JSONB, nullable=False) # {"en": "...", "fr": "..."}
    description = Column(JSONB) # {"en": "...", "fr": "..."}
    thumbnail_url = Column(String)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Multimedia(Base):
    __tablename__ = "multimedia"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(JSONB, nullable=False)
    media_url = Column(String, nullable=False)
    thumbnail_url = Column(String)
    type = Column(String) # photo, video
    category = Column(JSONB) # {"en": "Nature", "fr": "Nature"}
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class GovernanceMember(Base):
    __tablename__ = "governance_members"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(JSONB) # {"en": "...", "fr": "..."}
    bio = Column(JSONB)
    photo_url = Column(String)
    organ_id = Column(String) # ag, cd, pe, dg
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Inquiry(Base):
    __tablename__ = "inquiries"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String) # contact, volunteer, partner, newsletter
    name = Column(String)
    email = Column(String, nullable=False)
    subject = Column(String)
    message = Column(Text)
    data = Column(JSONB) # Extra fields for volunteer/partner
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LiveStat(Base):
    __tablename__ = "live_stats"
    id = Column(Integer, primary_key=True, index=True)
    label = Column(JSONB)
    value = Column(String)
    icon_name = Column(String)
    category = Column(String)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

