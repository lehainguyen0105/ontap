from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any, Generic, TypeVar

T = TypeVar('T')

# Quy chuẩn cấu trúc Response chung 4 trường
class StandardResponse(BaseModel, Generic[T]):
    statusCode: int
    error: Optional[str] = None
    message: str
    data: Optional[T] = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class ProductCreate(BaseModel):
    product_code: str = Field(..., min_length=4, max_length=10)
    name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(..., ge=0)
    category_id: int

class ProductUpdate(BaseModel):
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)

class ProductResponse(BaseModel):
    id: int
    product_code: str
    name: str
    price: float
    stock_quantity: int
    category_id: int
    category: Optional[CategoryResponse] = None

    model_config = ConfigDict(from_attributes=True)