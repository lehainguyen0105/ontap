from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.book_schema import BookCreateSchema, BookUpdateSchema, BookResponseSchema
import services.book_service as book_service

router = APIRouter(prefix="/api/v1/books", tags=["Books Management"])

# ==========================================
# 🟢 1. TRUY VẤN NÂNG CAO (ĐẶT TRƯỚC /{id})
# ==========================================

@router.get("/search", response_model=List[BookResponseSchema], status_code=status.HTTP_200_OK)
def search_books(
    query: str = Query(..., description="Từ khóa tìm kiếm theo Tiêu đề, Tác giả hoặc Thể loại"),
    db: Session = Depends(get_db)
):
    """6. Tìm kiếm mờ theo tiêu đề, tác giả hoặc thể loại (dùng ilike)"""
    return book_service.search_books(db, query)

@router.get("/borrow-warning", response_model=List[BookResponseSchema], status_code=status.HTTP_200_OK)
def borrow_warning(
    threshold: int = Query(5, description="Ngưỡng cảnh báo số lượng sách khả dụng trên kệ"),
    db: Session = Depends(get_db)
):
    """7. Cảnh báo sách có số lượng khả dụng trên kệ <= threshold (mặc định = 5)"""
    return book_service.get_borrow_warning_books(db, threshold)

@router.get("/top-borrowed", response_model=List[BookResponseSchema], status_code=status.HTTP_200_OK)
def top_borrowed(
    limit: int = Query(5, description="Số lượng top sách được mượn nhiều nhất cần lấy"),
    db: Session = Depends(get_db)
):
    """8. Báo cáo Top N cuốn sách được mượn nhiều nhất"""
    return book_service.get_top_borrowed_books(db, limit)

# ==========================================
# 🔵 2. THAO TÁC CRUD CƠ BẢN
# ==========================================

@router.post("", response_model=BookResponseSchema, status_code=status.HTTP_201_CREATED)
def create_book(book_in: BookCreateSchema, db: Session = Depends(get_db)):
    """1. Tạo mới một cuốn sách (Status 201 Created)"""
    return book_service.create_book(db, book_in)

@router.get("", response_model=List[BookResponseSchema], status_code=status.HTTP_200_OK)
def get_all_books(db: Session = Depends(get_db)):
    return book_service.get_all_books(db)

@router.get("/{id}", response_model=BookResponseSchema, status_code=status.HTTP_200_OK)
def get_book_by_id(id: int, db: Session = Depends(get_db)):
    db_book = book_service.get_book_by_id(db, id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sách với ID {id} không tồn tại!"
        )
    return db_book

@router.put("/{id}", response_model=BookResponseSchema, status_code=status.HTTP_200_OK)
def update_book(id: int, book_in: BookUpdateSchema, db: Session = Depends(get_db)):
    updated_book = book_service.update_book(db, id, book_in)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sách với ID {id} không tồn tại để cập nhật!"
        )
    return updated_book

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_book(id: int, db: Session = Depends(get_db)):
    success = book_service.delete_book(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sách với ID {id} không tồn tại để xóa!"
        )
    return {"message": f"Đã xóa thành công cuốn sách có ID {id}"}