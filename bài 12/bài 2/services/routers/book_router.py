from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.book_schema import BookCreateSchema, BookResponseSchema
import services.book_service as book_service

router = APIRouter(prefix="/api/v1/books", tags=["Books Management"])

@router.post("", response_model=BookResponseSchema, status_code=status.HTTP_201_CREATED)
def create_book(book_in: BookCreateSchema, db: Session = Depends(get_db)):
    return book_service.create_book(db, book_in)