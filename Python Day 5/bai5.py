from fastapi import FastAPI

app = FastAPI(title="Library Management API")


LIBRARY_DATA = {
    "ten_thu_vien": "Thư viện Rikkei",
    "dia_chi": "123 Nguyễn Văn Cừ, Hà Nội",
    "gio_mo_cua": "08:00 - 21:00"
}


@app.get("/api/v1/library-info")
def get_library_info():
    return LIBRARY_DATA