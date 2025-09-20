from sqlalchemy.orm import Session
from app.db.models.role import Role

def get_roles(db: Session, skip: int = 0, limit: int = 100):
    query = db.query(Role).offset(skip).limit(limit).all()
    total = db.query(Role).count()
    return total, query

def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()

def create_role(db: Session, role_data):
    role = Role(**role_data.dict())
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def update_role(db: Session, role_id: int, role_update):
    role = get_role(db, role_id)
    if not role:
        return None
    if role_update.name is not None:
        role.name = role_update.name
    if role_update.permissions is not None:
        role.permissions = role_update.permissions
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def delete_role(db: Session, role_id: int):
    role = get_role(db, role_id)
    if not role:
        return None
    db.delete(role)
    db.commit()
    return role
