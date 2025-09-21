# app/schemas/product.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    currency: str = Field(default="USD", max_length=3)

class AssignCategoryRequest(BaseModel):
    category_id: int

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    currency: str
    is_active: bool = True
    # category_id: Optional[int]
    category_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes=True
        orm_mode = True

class BulkDeleteRequest(BaseModel):
    product_ids: List[int]


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = True


# product review
class ProductReviewCreate(BaseModel):
    rating: float = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ProductReviewResponse(BaseModel):
    id: int
    product_id: int
    rating: float
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes=True
        orm_mode = True


# product image
class ProductImageResponse(BaseModel):
    id: int
    file_path: str
    created_at: datetime

    class Config:
        orm_mode = True
