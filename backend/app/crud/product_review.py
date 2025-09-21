# app/crud/product_review.py

from sqlalchemy.orm import Session
from typing import List
from app.db.models.product import ProductReview
from app.schemas.product import ProductReviewCreate

def add_review(db: Session, product_id: int, review_data: ProductReviewCreate) -> ProductReview:
    review = ProductReview(
        product_id=product_id,
        rating=review_data.rating,
        comment=review_data.comment
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def get_reviews(db: Session, product_id: int) -> List[ProductReview]:
    return db.query(ProductReview).filter(ProductReview.product_id == product_id).all()

def delete_review(db: Session, review_id: int) -> bool:
    review = db.query(ProductReview).filter(ProductReview.id == review_id).first()
    if not review:
        return False
    db.delete(review)
    db.commit()
    return True
