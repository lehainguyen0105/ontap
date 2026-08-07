from typing import List, Optional
from models.book_model import BookModel
from schemas.book_schema import BookCreateSchema, BookUpdateSchema
from sqlalchemy.orm import Session


def get_all_books(db: Session) -> List[BookModel]:
    return db.query(BookModel).all()


def get_book_by_id(db: Session, book_id: int) -> Optional[BookModel]:
    return db.query(BookModel).filter(BookModel.id == book_id).first()


def create_book(db: Session, book_data: BookCreateSchema) -> BookModel:
    new_book = BookModel(**book_data.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def update_book(
    db: Session, book_id: int, book_data: BookUpdateSchema
) -> Optional[BookModel]:
    book = get_book_by_id(db, book_id)
    if not book:
        return None

    update_dict = book_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int) -> bool:
    book = get_book_by_id(db, book_id)
    if not book:
        return False

    db.delete(book)
    db.commit()
    return True