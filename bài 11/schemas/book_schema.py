from pydantic import BaseModel, ConfigDict
from typing import Optional

class BookBaseSchema(BaseModel):
    title: str
    author: str
    category: str
    price: float
    borrow_count: Optional[int] = 0
    available_quantity: Optional[int] = 0

class BookCreateSchema(BookBaseSchema):
    pass

class BookUpdateSchema(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    borrow_count: Optional[int] = None
    available_quantity: Optional[int] = None

class BookResponseSchema(BookBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)