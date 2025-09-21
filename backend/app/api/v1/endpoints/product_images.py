from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.product import ProductImageResponse
from app.services import product_image_service

router = APIRouter()

@router.post("/{product_id}/images", response_model=List[ProductImageResponse])
def upload_product_images(
    product_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    images, error = product_image_service.upload_images(db, product_id, files)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return images

@router.get("/{product_id}/images", response_model=List[ProductImageResponse])
def list_product_images(product_id: int, db: Session = Depends(get_db)):
    return product_image_service.list_images(db, product_id)

@router.delete("/{product_id}/images/{image_id}")
def delete_product_image(product_id: int, image_id: int, db: Session = Depends(get_db)):
    image = product_image_service.delete_image(db, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"message": "Image deleted successfully"}
