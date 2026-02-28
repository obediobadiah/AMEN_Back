from sqlalchemy.orm import Session
from ..models.all_models import Project
from ..schemas.project import ProjectCreate, ProjectUpdate
from ..core.translate import multi_translate, translate_content, multi_translate_list
from typing import Optional

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Project).order_by(Project.created_at.desc()).offset(skip).limit(limit).all()

def get_project_by_id(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

# Removed _translate_list as it's now multi_translate_list in translate module

def create_project(db: Session, project: ProjectCreate):
    project_data = project.model_dump()
    # Read hint but let translation helpers decide
    source_lang_hint = project_data.pop("source_lang", None)
    
    # Auto-translate bilingual fields (ignoring hint to ensure auto-detection works per field)
    if isinstance(project_data.get("title"), str):
        project_data["title"] = multi_translate(project_data["title"])
    if isinstance(project_data.get("description"), str):
        project_data["description"] = multi_translate(project_data["description"])
    if isinstance(project_data.get("location"), str):
        project_data["location"] = multi_translate(project_data["location"])
    if isinstance(project_data.get("category"), str):
        project_data["category"] = multi_translate(project_data["category"])
    if isinstance(project_data.get("impact_stats"), str):
        project_data["impact_stats"] = multi_translate(project_data["impact_stats"])
    if isinstance(project_data.get("overview"), str):
        project_data["overview"] = multi_translate(project_data["overview"])
    
    # Handle lists
    if isinstance(project_data.get("goals"), list):
        project_data["goals"] = multi_translate_list(project_data["goals"])
    if isinstance(project_data.get("achievements"), list):
        project_data["achievements"] = multi_translate_list(project_data["achievements"])

    db_project = Project(**project_data)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db: Session, project_id: int, project: ProjectUpdate):
    db_project = get_project_by_id(db, project_id)
    if not db_project:
        return None
    
    update_data = project.model_dump(exclude_unset=True)
    # Hint is ignored now to favor auto-detection
    update_data.pop("source_lang", None)
    
    # Handle re-translation if flat strings or lists are provided
    if isinstance(update_data.get("title"), str):
        update_data["title"] = multi_translate(update_data["title"])
    if isinstance(update_data.get("description"), str):
        update_data["description"] = multi_translate(update_data["description"])
    if isinstance(update_data.get("location"), str):
        update_data["location"] = multi_translate(update_data["location"])
    if isinstance(update_data.get("category"), str):
        update_data["category"] = multi_translate(update_data["category"])
    if isinstance(update_data.get("impact_stats"), str):
        update_data["impact_stats"] = multi_translate(update_data["impact_stats"])
    if isinstance(update_data.get("overview"), str):
        update_data["overview"] = multi_translate(update_data["overview"])
    
    if isinstance(update_data.get("goals"), list):
        update_data["goals"] = multi_translate_list(update_data["goals"])
    if isinstance(update_data.get("achievements"), list):
        update_data["achievements"] = multi_translate_list(update_data["achievements"])
        
    for key, value in update_data.items():
        setattr(db_project, key, value)
        
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int):
    db_project = get_project_by_id(db, project_id)
    if not db_project:
        return None
    db.delete(db_project)
    db.commit()
    return db_project
