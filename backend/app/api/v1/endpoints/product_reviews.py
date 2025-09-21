# app/api/v1/endpoints/product_reviews.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.product import ProductReviewCreate, ProductReviewResponse
from app.services import product_review_service
from app.db.session import get_db

router = APIRouter()

@router.post("/products/{product_id}/reviews", response_model=ProductReviewResponse)
def add_review(product_id: int, review: ProductReviewCreate, db: Session = Depends(get_db)):
    return product_review_service.add_review(db, product_id, review)

@router.get("/products/{product_id}/reviews", response_model=List[ProductReviewResponse])
def list_reviews(product_id: int, db: Session = Depends(get_db)):
    return product_review_service.get_reviews(db, product_id)

@router.delete("/products/{product_id}/reviews/{review_id}")
def delete_review(product_id: int, review_id: int, db: Session = Depends(get_db)):
    success = product_review_service.delete_review(db, review_id)
    if not success:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review deleted successfully"}
