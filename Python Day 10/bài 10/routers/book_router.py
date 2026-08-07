from typing import List
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.book_schema import (
    BookCreateSchema,
    BookResponseSchema,
    BookUpdateSchema,
)
from services import book_service
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/books", tags=["Book Controller"])


@router.get("", response_model=List[BookResponseSchema])
def get_books(db: Session = Depends(get_db)):
    return book_service.get_all_books(db)


@router.get("/{book_id}", response_model=BookResponseSchema)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = book_service.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy cuốn sách",
        )
    return book


@router.post(
    "",
    response_model=BookResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_new_book(
    book_data: BookCreateSchema, db: Session = Depends(get_db)
):
    return book_service.create_book(db, book_data)


@router.put("/{book_id}", response_model=BookResponseSchema)
def update_existing_book(
    book_id: int,
    book_data: BookUpdateSchema,
    db: Session = Depends(get_db),
):
    updated_book = book_service.update_book(db, book_id, book_data)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy cuốn sách để cập nhật",
        )
    return updated_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_book(book_id: int, db: Session = Depends(get_db)):
    success = book_service.delete_book(db, book_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy cuốn sách để xóa",
        )
    return None