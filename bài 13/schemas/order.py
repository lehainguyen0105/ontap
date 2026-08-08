from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=1)
    items: List[OrderItemCreate] = Field(..., min_items=1)

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: Optional[str] = None
    quantity: int
    unit_price: float

class OrderResponse(BaseModel):
    id: int
    order_code: str
    customer_name: str
    total_amount: float
    status: str
    items: List[OrderItemResponse] = []

    model_config = ConfigDict(from_attributes=True)