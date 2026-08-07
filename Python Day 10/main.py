from database import Base, engine
from fastapi import FastAPI
from routers import book_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management System",
    description="Hệ thống quản lý thư viện chuẩn kiến trúc 4 lớp",
    version="1.0.0",
)

app.include_router(book_router.router)


@app.get("/")
def root():
    return {"message": "Chào mừng đến với API Quản lý thư viện!"}