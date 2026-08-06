from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = "mysql+pymysql://root:lehainguyen0105@localhost:3306/library_management"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    price: float
    quantity: int

    model_config = ConfigDict(from_attributes=True)

def update_book(db: Session, book_id: int, book_in: BookUpdate):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        return None

    update_data = book_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int) -> bool:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        return False

    db.delete(db_book)
    db.commit()
    return True

app = FastAPI(title="Library Management API")

@app.put("/books/{id}", response_model=BookResponse)
def update_book_endpoint(id: int, book_in: BookUpdate, db: Session = Depends(get_db)):
    updated_book = update_book(db, book_id=id, book_in=book_in)
    if updated_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sách không tồn tại trong hệ thống"
        )
    return updated_book

@app.delete("/books/{id}")
def delete_book_endpoint(id: int, db: Session = Depends(get_db)):
    success = delete_book(db, book_id=id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sách không tồn tại trong hệ thống"
        )
    return {"message": f"Đã xóa thành công sách ID {id}"}