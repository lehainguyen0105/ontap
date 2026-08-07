from typing import Optional
from pydantic import BaseModel, ConfigDict


class BookBaseSchema(BaseModel):
    title: str
    author: str
    price: float
    quantity: Optional[int] = 0


class BookCreateSchema(BookBaseSchema):
    pass


class BookUpdateSchema(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


class BookResponseSchema(BookBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)