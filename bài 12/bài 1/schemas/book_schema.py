from pydantic import BaseModel, ConfigDict
from typing import Optional
from schemas.author_schema import AuthorResponseSchema

class BookCreateSchema(BaseModel):
    title: str
    price: float
    author_id: int
    borrow_count: Optional[int] = 0
    available_quantity: Optional[int] = 10

class BookResponseSchema(BaseModel):
    id: int
    title: str
    price: float
    author_id: int
    author: AuthorResponseSchema

    model_config = ConfigDict(from_attributes=True)