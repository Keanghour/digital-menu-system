# app/api/v1/endpoints/products.py

import io
import os
import shutil
from datetime import datetime
from fastapi import APIRouter, Body, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.product import BulkDeleteRequest, ProductCreate, ProductResponse, AssignCategoryRequest, ProductUpdate
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


@router.delete("/", summary="Delete multiple products")
def bulk_delete_products_endpoint(
    data: BulkDeleteRequest,
    db: Session = Depends(get_db)
):
    return product_service.bulk_delete_products(db, data)


@router.put("/{product_id}", summary="Update product by ID")
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    updated_product = product_service.update_product(db, product_id, product_data)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated successfully", "product": updated_product}


@router.delete("/{product_id}/category", summary="Remove product from category")
def remove_product_category(product_id: int, db: Session = Depends(get_db)):
    product = product_service.remove_product_category(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product removed from category successfully", "product": product}


@router.get("/products/", summary="List products with pagination and filters")
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    name: str | None = None,
    category_id: int | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db)
):
    products, total = product_service.get_products(
        db, skip=skip, limit=limit, name=name, category_id=category_id, is_active=is_active
    )
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "products": products
    }


@router.get("/export", summary="Export products as CSV or Excel")
def export_products(format: str = Query("csv", enum=["csv", "xlsx"]), db: Session = Depends(get_db)):
    content, mime_type = product_service.export_products(db, file_format=format)

    if format == "csv":
        return StreamingResponse(
            io.StringIO(content),
            media_type=mime_type,
            headers={"Content-Disposition": "attachment; filename=products.csv"}
        )
    else:  # xlsx
        return StreamingResponse(
            io.BytesIO(content),
            media_type=mime_type,
            headers={"Content-Disposition": "attachment; filename=products.xlsx"}
        )
    

# @router.post("/import", summary="Import products from CSV or Excel")
# def import_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     try:
#         if file.filename.endswith(".csv"):
#             products = product_service.import_products(db, file, "csv")
#         elif file.filename.endswith(".xlsx"):
#             products = product_service.import_products(db, file, "xlsx")
#         else:
#             raise HTTPException(status_code=400, detail="Invalid file format. Use .csv or .xlsx")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Import failed: {str(e)}")

#     return {"message": f"Imported {len(products)} products successfully"}


UPLOAD_DIR = "uploads"


@router.post("/import", summary="Import products from CSV or Excel")
def import_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save file with timestamp
    file_path = os.path.join(UPLOAD_DIR, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Re-open for processing
    with open(file_path, "rb") as f:
        if file.filename.endswith(".csv"):
            products = product_service.import_products(db, UploadFile(file=f, filename=file.filename), "csv")
        elif file.filename.endswith(".xlsx"):
            products = product_service.import_products(db, UploadFile(file=f, filename=file.filename), "xlsx")
        else:
            raise HTTPException(status_code=400, detail="Invalid file format. Use .csv or .xlsx")

    return {"message": f"Imported {len(products)} products successfully", "file_path": file_path}



@router.delete("/{product_id}", response_model=ProductResponse)
def soft_delete_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


