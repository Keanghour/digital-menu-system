# app/crud/product.py

from typing import List
from sqlalchemy.orm import Session
from app.db.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def create_product(db: Session, data: ProductCreate):
    product = Product(
        name=data.name,
        description=data.description,
        price=data.price,
        currency=data.currency
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def list_products(db: Session, limit: int = None):
    query = db.query(Product)
    if limit:
        query = query.limit(limit)
    return query.all()

def assign_category(db: Session, product_id: int, category_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None, "Product not found"
    product.category_id = category_id
    db.add(product)
    db.commit()
    db.refresh(product)
    return product, None

def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return 0
    db.delete(product)
    db.commit()
    return 1



def bulk_delete_products(db: Session, product_ids: List[int]) -> dict:
    existing_products = db.query(Product).filter(Product.id.in_(product_ids)).all()
    existing_ids = [p.id for p in existing_products]
    
    if existing_products:
        for product in existing_products:
            db.delete(product)
        db.commit()

    not_found_ids = list(set(product_ids) - set(existing_ids))
    
    return {
        "deleted": len(existing_ids),
        "not_found": not_found_ids
    }


def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    for field, value in product_data.dict(exclude_unset=True).items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


def remove_product_category(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    
    product.category_id = None  # remove the relation
    db.commit()
    db.refresh(product)
    return product


def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    name: str | None = None,
    category_id: int | None = None,
    is_active: bool | None = None
):
    query = db.query(Product)

    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if is_active is not None:
        query = query.filter(Product.is_active == is_active)

    total = query.count()
    products = query.offset(skip).limit(limit).all()
    return products, total


def get_all_products(db: Session):
    return db.query(Product).all()


def get_stock(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def update_stock(db: Session, product_id: int, stock: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    product.stock = stock
    db.commit()
    db.refresh(product)
    return product


