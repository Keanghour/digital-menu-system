from sqlalchemy.orm import Session
from app.crud import category as category_crud
from app.schemas.category import CategoryCreate
from fastapi import HTTPException

# ----------------------------
# Create Category
# ----------------------------
def create_category(db: Session, request: CategoryCreate):
    existing = category_crud.get_category_by_name(db, request.name)
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    return category_crud.create_category(db, request)


# ----------------------------
# List / Get Categories
# ----------------------------
def list_categories(db: Session, limit: int = None):
    return category_crud.get_categories(db, limit)

def get_category(db: Session, category_id: int):
    category = category_crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


# ----------------------------
# Update / Replace Category
# ----------------------------
def update_category(db: Session, category_id: int, request: CategoryCreate):
    category = category_crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category.name = request.name
    category.description = request.description
    db.commit()
    db.refresh(category)
    return category


# ----------------------------
# Delete Category
# ----------------------------
def delete_category(db: Session, category_id: int):
    category, error = category_crud.delete_category(db, category_id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return category
