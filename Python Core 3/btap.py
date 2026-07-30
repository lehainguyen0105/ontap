inventory = [
    {"id": "SP1", "ten": "Tai nghe Sony", "gia": 1200000, "danh_muc": "Phụ kiện"},
    {"id": "SP2", "ten": "Chuột không dây", "gia": 450000, "danh_muc": "Phụ kiện"},
    {"id": "SP3", "ten": "Bàn phím Cơ", "gia": 950000, "danh_muc": "Phụ kiện"},
    {"id": "SP4", "ten": "Màn hình Dell 27 inch", "gia": 4500000, "danh_muc": "Thiết bị"},
    {"id": "SP5", "ten": "Sạc dự phòng 20000mAh", "gia": 350000, "danh_muc": "Phụ kiện"}
]

students = [
    {"name": "An", "gpa": 7.2},
    {"name": "Bình", "gpa": 9.5},
    {"name": "Cường", "gpa": 6.8},
    {"name": "Dũng", "gpa": 8.4}
]

def linear_search_filter(cart, target_category, max_price):
    result = []
    for item in cart:
        if item["danh_muc"] == target_category and item["gia"] <= max_price:
            result.append(item)
    return result

category_target = "Phụ kiện"
max_price_target = 1000000

filtered_products = linear_search_filter(inventory, category_target, max_price_target)

print("KẾT QUẢ LỌC SẢN PHẨM (LINEAR SEARCH MULTI-CRITERIA)")
print(f"Danh mục tìm kiếm: {category_target} | Giá tối đa: {max_price_target:,} VNĐ")
print(f"Tìm thấy {len(filtered_products)} sản phẩm phù hợp:")
for item in filtered_products:
    print(f"  -> [{item['id']}] {item['ten']} | Giá: {item['gia']:,} VNĐ")

print("\n" + "="*50 + "\n")

def bubble_sort_students_desc(student_list):
    arr = student_list.copy()
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j]["gpa"] < arr[j + 1]["gpa"]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

sorted_students = bubble_sort_students_desc(students)

print("BẢNG XẾP HẠNG SINH VIÊN (BUBBLE SORT - GPA GIẢM DẦN)")
for idx, student in enumerate(sorted_students, 1):
    print(f"Top {idx}: {student['name']} - {student['gpa']} điểm")