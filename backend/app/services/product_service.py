from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.product import ProductCreate, ProductResponse
from app.crud import product as product_crud

def create_product(db: Session, data: ProductCreate) -> ProductResponse:
    product = product_crud.create_product(db, data)
    return ProductResponse.from_orm(product)

def get_product(db: Session, product_id: int) -> Optional[ProductResponse]:
    product = product_crud.get_product(db, product_id)
    if not product:
        return None
    category_name = product.category.name if product.category else None
    return ProductResponse.from_orm(product).copy(update={"category_name": category_name})

def list_products(db: Session, limit: int = None) -> List[ProductResponse]:
    products = product_crud.list_products(db, limit)
    result = []
    for p in products:
        category_name = p.category.name if p.category else None
        result.append(ProductResponse.from_orm(p).copy(update={"category_name": category_name}))
    return result

def assign_category(db: Session, product_id: int, category_id: int) -> ProductResponse:
    product, error = product_crud.assign_category(db, product_id, category_id)
    if error:
        raise Exception(error)
    category_name = product.category.name if product.category else None
    return ProductResponse.from_orm(product).copy(update={"category_name": category_name})

def delete_product(db: Session, product_id: int) -> dict:
    deleted = product_crud.delete_product(db, product_id)
    if not deleted:
        return {"deleted": 0, "message": "Product not found"}
    return {"deleted": 1, "message": "Product deleted successfully"}

