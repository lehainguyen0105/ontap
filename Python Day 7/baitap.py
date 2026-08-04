from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Library Books Management API",
    description="API CRUD Quản lý sách thư viện",
    version="1.0.0"
)

class Book(BaseModel):
    id: int
    ten_sach: str
    tac_gia: str
    nam_xuat_ban: int
    so_luong: int

danh_sach_sach: List[Book] = [
    Book(
        id=1,
        ten_sach="Nhà Giả Kim",
        tac_gia="Paulo Coelho",
        nam_xuat_ban=1988,
        so_luong=5
    ),
    Book(
        id=2,
        ten_sach="Tôi Thấy Hoa Vàng Trên Cỏ Xanh",
        tac_gia="Nguyễn Nhật Ánh",
        nam_xuat_ban=2010,
        so_luong=8
    ),
    Book(
        id=3,
        ten_sach="Rừng Na Uy",
        tac_gia="Haruki Murakami",
        nam_xuat_ban=1987,
        so_luong=3
    )
]

@app.post(
    "/api/v1/books", 
    response_model=Book, 
    status_code=status.HTTP_201_CREATED,
    summary="Thêm mới một cuốn sách"
)
def create_book(book: Book):
    for b in danh_sach_sach:
        if b.id == book.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Sách với id {book.id} đã tồn tại!"
            )
    danh_sach_sach.append(book)
    return book

@app.get(
    "/api/v1/books", 
    response_model=List[Book],
    summary="Lấy danh sách tất cả cuốn sách"
)
def get_all_books():
    return danh_sach_sach

@app.get(
    "/api/v1/books/{book_id}", 
    response_model=Book,
    summary="Lấy chi tiết cuốn sách theo ID"
)
def get_book_by_id(book_id: int):
    for book in danh_sach_sach:
        if book.id == book_id:
            return book
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Không tìm thấy sách với id: {book_id}"
    )

@app.put(
    "/api/v1/books/{book_id}", 
    response_model=Book,
    summary="Cập nhật thông tin cuốn sách theo ID"
)
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(danh_sach_sach):
        if book.id == book_id:
            danh_sach_sach[index] = updated_book
            return updated_book
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Không tìm thấy sách với id: {book_id}"
    )

@app.delete(
    "/api/v1/books/{book_id}", 
    response_model=dict,
    summary="Xóa một cuốn sách theo ID"
)
def delete_book(book_id: int):
    for index, book in enumerate(danh_sach_sach):
        if book.id == book_id:
            danh_sach_sach.pop(index)
            return {"message": f"Đã xóa thành công sách có id: {book_id}"}
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Không tìm thấy sách với id: {book_id}"
    )