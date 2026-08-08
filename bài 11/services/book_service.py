from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.book_model import BookModel
from schemas.book_schema import BookCreateSchema, BookUpdateSchema
from typing import List, Optional

def get_all_books(db: Session) -> List[BookModel]:
    return db.query(BookModel).all()

def get_book_by_id(db: Session, book_id: int) -> Optional[BookModel]:
    return db.query(BookModel).filter(BookModel.id == book_id).first()

def create_book(db: Session, book_in: BookCreateSchema) -> BookModel:
    db_book = BookModel(**book_in.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book_in: BookUpdateSchema) -> Optional[BookModel]:
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None
    
    update_data = book_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)
        
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int) -> bool:
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return False
    db.delete(db_book)
    db.commit()
    return True

def search_books(db: Session, query_str: str) -> List[BookModel]:
    return db.query(BookModel).filter(
        or_(
            BookModel.title.ilike(f"%{query_str}%"),
            BookModel.author.ilike(f"%{query_str}%"),
            BookModel.category.ilike(f"%{query_str}%")
        )
    ).all()

def get_borrow_warning_books(db: Session, threshold: int = 5) -> List[BookModel]:
    return db.query(BookModel).filter(BookModel.available_quantity <= threshold).all()

def get_top_borrowed_books(db: Session, limit: int = 5) -> List[BookModel]:
    return db.query(BookModel).order_by(BookModel.borrow_count.desc()).limit(limit).all()