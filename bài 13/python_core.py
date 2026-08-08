import re

raw_products = [
    {"product_code": "P301", "name": "Laptop Dell XPS", "price": 25000000, "stock": 10, "status": "available"},
    {"product_code": " p101 ", "name": "Chuột Logitech", "price": 500000, "stock": 50, "status": "available"},
    {"product_code": "P202", "name": "Màn hình LG 27", "price": 6000000, "stock": 0, "status": "out_of_stock"},
    {"product_code": "P102", "name": "Bàn phím Cơ", "price": 1200000, "stock": 15, "status": "available"},
    {"product_code": "P302", "name": "Tai nghe Sony", "price": 3500000, "stock": 8, "status": "available"}
]

raw_orders = [
    {"order_code": "ORD001", "customer": "Nguyễn Văn A", "amount": 15000000, "status": "COMPLETED"},
    {"order_code": "ORD002", "customer": "Trần Thị B", "amount": 25000000, "status": "COMPLETED"},
    {"order_code": "ORD003", "customer": "Lê Văn C", "amount": 8000000, "status": "PENDING"},
    {"order_code": "ORD004", "customer": "Phạm Văn D", "amount": 45000000, "status": "COMPLETED"}
]

def clean_and_validate_products(products: list) -> list:
    valid_products = []
    pattern = r"^[P|p]\d{3}$"
    
    for item in products:
        cleaned_item = item.copy()
        raw_code = cleaned_item.get("product_code", "").strip().upper()
        cleaned_item["product_code"] = raw_code
        
        if re.match(pattern, raw_code):
            valid_products.append(cleaned_item)
            
    return valid_products

def binary_search_product(products: list, target_code: str):
    left = 0
    right = len(products) - 1
    target = target_code.strip().upper()
    
    while left <= right:
        mid = (left + right) // 2
        current_code = products[mid]["product_code"]
        
        if current_code == target:
            return products[mid]
        elif current_code < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return None

def sort_products_by_price_desc(products: list) -> list:
    if len(products) <= 1:
        return products
    
    pivot = products[len(products) // 2]
    pivot_price = pivot["price"]
    
    left = [x for x in products if x["price"] > pivot_price]
    middle = [x for x in products if x["price"] == pivot_price]
    right = [x for x in products if x["price"] < pivot_price]
    
    return sort_products_by_price_desc(left) + middle + sort_products_by_price_desc(right)

def analyze_order_stats(orders: list) -> dict:
    total_revenue = 0
    max_order = None
    max_amount = -1
    
    for order in orders:
        if order.get("status") == "COMPLETED":
            total_revenue += order.get("amount", 0)
            
        if order.get("amount", 0) > max_amount:
            max_amount = order.get("amount", 0)
            max_order = order
            
    return {
        "total_revenue": total_revenue,
        "max_order": max_order
    }