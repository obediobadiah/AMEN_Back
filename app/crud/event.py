from sqlalchemy.orm import Session
from ..models.all_models import Event
from ..schemas.event import EventCreate, EventUpdate
from ..core.translate import multi_translate

def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Event).order_by(Event.id.desc()).offset(skip).limit(limit).all()

def get_event_by_id(db: Session, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()

def create_event(db: Session, event: EventCreate):
    event_data = event.model_dump()
    source_lang = event_data.pop("source_lang", "fr")
    
    event_data["title"] = multi_translate(event_data["title"], source_lang)
    if event_data.get("description"):
        event_data["description"] = multi_translate(event_data["description"], source_lang)
    if event_data.get("location"):
        event_data["location"] = multi_translate(event_data["location"], source_lang)
        
    db_event = Event(**event_data)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def update_event(db: Session, event_id: int, event: EventUpdate):
    db_event = get_event_by_id(db, event_id)
    if not db_event:
        return None
        
    update_data = event.model_dump(exclude_unset=True)
    source_lang = update_data.pop("source_lang", "fr")
    
    if isinstance(update_data.get("title"), str):
        update_data["title"] = multi_translate(update_data["title"], source_lang)
    if isinstance(update_data.get("description"), str):
        update_data["description"] = multi_translate(update_data["description"], source_lang)
    if isinstance(update_data.get("location"), str):
        update_data["location"] = multi_translate(update_data["location"], source_lang)
        
    for key, value in update_data.items():
        setattr(db_event, key, value)
        
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int):
    db_event = get_event_by_id(db, event_id)
    if not db_event:
        return None
    db.delete(db_event)
    db.commit()
    return db_event
