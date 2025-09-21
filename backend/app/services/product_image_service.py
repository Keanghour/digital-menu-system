import os
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.crud import product_image as image_crud
from app.db.models.product import Product

UPLOAD_DIR = "uploads/products"

def save_product_image_file(file: UploadFile, product_id: int) -> str:
    os.makedirs(f"{UPLOAD_DIR}/{product_id}", exist_ok=True)
    file_path = f"{UPLOAD_DIR}/{product_id}/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return file_path

def upload_images(db: Session, product_id: int, files: list[UploadFile]):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None, "Product not found"

    saved_images = []
    for file in files:
        path = save_product_image_file(file, product_id)
        image = image_crud.add_product_image(db, product_id, path)
        saved_images.append(image)
    return saved_images, None

def list_images(db: Session, product_id: int):
    return image_crud.get_product_images(db, product_id)

def delete_image(db: Session, image_id: int):
    image = image_crud.delete_product_image(db, image_id)
    if image and os.path.exists(image.file_path):
        os.remove(image.file_path)
    return image
