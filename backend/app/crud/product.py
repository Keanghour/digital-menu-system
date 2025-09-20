from sqlalchemy.orm import Session
from app.db.models.product import Product
from app.schemas.product import ProductCreate

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

