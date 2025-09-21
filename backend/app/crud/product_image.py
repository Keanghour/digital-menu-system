from sqlalchemy.orm import Session
from app.db.models.product import ProductImage

def add_product_image(db: Session, product_id: int, file_path: str) -> ProductImage:
    image = ProductImage(product_id=product_id, file_path=file_path)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

def get_product_images(db: Session, product_id: int):
    return db.query(ProductImage).filter(ProductImage.product_id == product_id).all()

def delete_product_image(db: Session, image_id: int):
    image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if image:
        db.delete(image)
        db.commit()
    return image
