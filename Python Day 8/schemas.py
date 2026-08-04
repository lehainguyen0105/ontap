from pydantic import BaseModel

class BookCreate(BaseModel):
    code: str
    title: str
    price: float
    pages: int

class BookResponse(BookCreate):
    id: int

    class Config:
        from_attributes = True