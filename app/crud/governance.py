from sqlalchemy.orm import Session
from ..models.all_models import GovernanceMember
from ..schemas.governance import GovernanceCreate, GovernanceUpdate

def get_members(db: Session, skip: int = 0, limit: int = 100, organ_id: str = None):
    query = db.query(GovernanceMember)
    if organ_id:
        query = query.filter(GovernanceMember.organ_id == organ_id)
    return query.order_by(GovernanceMember.order).offset(skip).limit(limit).all()

def get_member_by_id(db: Session, member_id: int):
    return db.query(GovernanceMember).filter(GovernanceMember.id == member_id).first()

def create_member(db: Session, member: GovernanceCreate):
    db_member = GovernanceMember(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def update_member(db: Session, member_id: int, member: GovernanceUpdate):
    db_member = get_member_by_id(db, member_id)
    if not db_member:
        return None
    for key, value in member.model_dump(exclude_unset=True).items():
        setattr(db_member, key, value)
    db.commit()
    db.refresh(db_member)
    return db_member

def delete_member(db: Session, member_id: int):
    db_member = get_member_by_id(db, member_id)
    if not db_member:
        return None
    db.delete(db_member)
    db.commit()
    return db_member
