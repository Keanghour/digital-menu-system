from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.product import ProductCreate, ProductResponse, AssignCategoryRequest
from app.db.session import get_db
from app.services import product_service

router = APIRouter()

@router.post("", response_model=ProductResponse)
def create_product_endpoint(request: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, request)

@router.post("/{product_id}/category", response_model=ProductResponse)
def assign_category_endpoint(product_id: int, request: AssignCategoryRequest, db: Session = Depends(get_db)):
    try:
        return product_service.assign_category(db, product_id, request.category_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{product_id}", response_model=ProductResponse)
def get_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("", response_model=List[ProductResponse])
def list_products_endpoint(limit: Optional[int] = None, db: Session = Depends(get_db)):
    return product_service.list_products(db, limit)

@router.delete("/{product_id}")
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    return product_service.delete_product(db, product_id)



