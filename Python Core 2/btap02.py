orders = [
    {"id": "DH01", "name": "iPhone 15 Pro Max", "price": 32000000},
    {"id": "DH02", "name": "Tai nghe AirPods Pro", "price": 5500000},
    {"id": "DH03", "name": "MacBook Pro M3 Max", "price": 65000000},
    {"id": "DH04", "name": "Chuot khong day", "price": 450000},
    {"id": "DH05", "name": "Samsung Galaxy S24", "price": 22000000}
]

students_raw = [
    {"id": "SV01", "name": "  Nguyen Van An  ", "email": "an.nguyen@rikkei.edu.vn  ", "phone": "0987654321"},
    {"id": "SV02", "name": "Tran Thi Bich", "email": "bich_gmail.com", "phone": "0912345678"},
    {"id": "SV03", "name": "Le Hoang Cuong", "email": "cuong@gmail.com", "phone": "09876abcde"},
    {"id": "SV04", "name": "Pham Minh Dung", "email": "dung@gmail.com ", "phone": "0355667788 "}
]

total_revenue = 0
vip_count = 0
is_suspicious = False

max_order = orders[0]
min_order = orders[0]

for order in orders:
    price = order["price"]
    
    total_revenue += price
    
    if price >= 15000000:
        vip_count += 1
        
    if price > max_order["price"]:
        max_order = order
    if price < min_order["price"]:
        min_order = order
        
    if price > 50000000:
        is_suspicious = True
        suspicious_order = order

print(f"Tong doanh thu: {total_revenue:,} VND")
print(f"So don hang VIP (>= 15tr): {vip_count} don")
print(f"Don hang gia tri CAO NHAT: {max_order['id']} - {max_order['name']} ({max_order['price']:,} VND)")
print(f"Don hang gia tri THAP NHAT: {min_order['id']} - {min_order['name']} ({min_order['price']:,} VND)")

if is_suspicious:
    print(f"CANH BAO RUI RO: Phat hien don {suspicious_order['id']} co gia tri {suspicious_order['price']:,} VND > 50tr!")
print(f"KET LUAN CAM CO: Co is_suspicious = {is_suspicious}")

print("\n" + "="*50 + "\n")

for sv in students_raw:
    clean_name = sv["name"].strip()
    clean_email = sv["email"].strip().lower()
    clean_phone = sv["phone"].strip()
    
    is_email_valid = ("@" in clean_email) and (clean_email.count("@") == 1) and \
                     (clean_email.endswith(".com") or clean_email.endswith(".edu.vn"))
                     
    is_phone_valid = (len(clean_phone) == 10) and clean_phone.startswith("0") and clean_phone.isdigit()
    
    if is_email_valid and is_phone_valid:
        status = "HO SO HOP LE"
    else:
        reasons = []
        if not is_email_valid:
            reasons.append("Thieu @" if "@" not in clean_email else "Email sai dinh dang")
        if not is_phone_valid:
            reasons.append("SDT chua chu" if not clean_phone.isdigit() else "SDT sai do dai/dau so")
        status = f"KHONG HOP LE ({', '.join(reasons)})"
        
    print(f"[{sv['id']}] {clean_name} | Email: {clean_email} | SDT: {clean_phone} -> {status}")