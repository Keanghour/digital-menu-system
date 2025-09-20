from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models.category import Category
from app.schemas.category import CategoryCreate

def create_category(db: Session, category: CategoryCreate) -> Category:
    db_category = Category(name=category.name, description=category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category(db: Session, category_id: int) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    return db.query(Category).offset(skip).limit(limit).all()

def update_category(db: Session, category_id: int, category_data: CategoryCreate) -> Category | None:
    category = get_category(db, category_id)
    if not category:
        return None
    category.name = category_data.name
    category.description = category_data.description
    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, category_id: int) -> bool:
    category = get_category(db, category_id)
    if not category:
        return False
    db.delete(category)
    db.commit()
    return True
