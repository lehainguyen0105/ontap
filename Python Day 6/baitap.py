from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Library Management API")

# ==========================================
# 1. BÀI 1: ĐỊNH NGHĨA PYDANTIC SCHEMAS
# ==========================================

class BookCreate(BaseModel):
    title: str
    author: str
    price: float
    pages: int

class BookResponse(BookCreate):
    id: int


# ==========================================
# 2. BÀI 2: GIẢ LẬP DATABASE & API ENDPOINTS
# ==========================================

books_db = []
book_id_counter = 1


@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate):
    global book_id_counter
    
    new_book_data = book.model_dump()
    new_book_data["id"] = book_id_counter
    
    books_db.append(new_book_data)
    
    book_id_counter += 1
    
    return new_book_data


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book
            
    raise HTTPException(status_code=404, detail="Book not found")