from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.book_model import BookModel
from models.author_model import AuthorModel
from schemas.book_schema import BookCreateSchema

def create_book(db: Session, book_in: BookCreateSchema) -> BookModel:
    author = db.query(AuthorModel).filter(AuthorModel.id == book_in.author_id).first()
    
    if not author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Mã tác giả author_id = {book_in.author_id} không tồn tại trong hệ thống CSDL!"
        )
    
    db_book = BookModel(**book_in.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book