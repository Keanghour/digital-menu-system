# app/services/product_review_service.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud import product_review as review_crud
from app.schemas.product import ProductReviewCreate, ProductReviewResponse

def add_review(db: Session, product_id: int, data: ProductReviewCreate) -> ProductReviewResponse:
    review = review_crud.add_review(db, product_id, data)
    return ProductReviewResponse.from_orm(review)

def get_reviews(db: Session, product_id: int) -> List[ProductReviewResponse]:
    reviews = review_crud.get_reviews(db, product_id)
    return [ProductReviewResponse.from_orm(r) for r in reviews]

def delete_review(db: Session, review_id: int) -> bool:
    return review_crud.delete_review(db, review_id)
