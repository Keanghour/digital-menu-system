# app/services/product_service.py

import csv
import io
from turtle import pd
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models.product import Product
from app.schemas.product import BulkDeleteRequest, ProductCreate, ProductResponse, ProductUpdate
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



def bulk_delete_products(db: Session, data: BulkDeleteRequest) -> dict:
    return product_crud.bulk_delete_products(db, data.product_ids)


def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    return product_crud.update_product(db, product_id, product_data)


def remove_product_category(db: Session, product_id: int):
    return product_crud.remove_product_category(db, product_id)

def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    name: str | None = None,
    category_id: int | None = None,
    is_active: bool | None = None
):
    return product_crud.get_products(db, skip, limit, name, category_id, is_active)


def export_products(db: Session, file_format: str = "csv"):
    products = product_crud.get_all_products(db)
    data = [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "category_id": p.category_id,
            "is_active": p.is_active,
        }
        for p in products
    ]

    if file_format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys() if data else [])
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue(), "text/csv"
    
    elif file_format == "xlsx":
        output = io.BytesIO()
        df = pd.DataFrame(data)
        df.to_excel(output, index=False)
        output.seek(0)
        return output.read(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    else:
        raise ValueError("Unsupported format")
    


def import_products(db: Session, file, file_format: str):
    if file_format == "csv":
        df = pd.read_csv(file.file)
    elif file_format == "xlsx":
        df = pd.read_excel(file.file)
    else:
        raise ValueError("Unsupported file format")

    created_products = []
    for _, row in df.iterrows():
        product = Product(
            name=row["name"],
            description=row.get("description", ""),
            price=row["price"],
            category_id=row.get("category_id"),
            is_active=row.get("is_active", True)
        )
        db.add(product)
        created_products.append(product)
    
    db.commit()
    return created_products


