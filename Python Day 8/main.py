from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import BookModel
from schemas import BookCreate, BookResponse
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System")

@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    existing_book = db.query(BookModel).filter(BookModel.code == book.code).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="Mã sách (code) đã tồn tại!")

    db_book = BookModel(
        code=book.code,
        title=book.title,
        price=book.price,
        pages=book.pages
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
def get_books(db: Session = Depends(get_db)):
    books = db.query(BookModel).all()
    return books