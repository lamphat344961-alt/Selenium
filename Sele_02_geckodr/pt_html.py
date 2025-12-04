from bs4 import BeautifulSoup

# 1. Đọc file HTML đã lưu từ bước Selenium trước đó
# (Bạn cần đảm bảo file 'raw_facebook_posts.html' đang nằm cùng thư mục với file code này)
try:
    with open(r"C:\Users\Admin\Desktop\TANPHAT\Manguonmotrongkhoahocjdulieu\facebook_raw.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    print("✅ Đã đọc file HTML thành công.")
except FileNotFoundError:
    print("❌ Lỗi: Không tìm thấy file 'raw_facebook_posts.html'. Hãy chạy bước lưu Selenium trước!")
    exit()

# 2. "Nấu súp" (Chuyển text thành object)
soup = BeautifulSoup(html_content, "html.parser")

# 3. THỰC HIỆN TÌM KIẾM
# Selenium XPath: //div[contains(@class, 'x1lliihq')]
# BeautifulSoup:  find_all("div", class_="x1lliihq")
# Lưu ý: class_ có dấu gạch dưới ở cuối
print("Đang tìm kiếm các thẻ div có class 'x1lliihq'...")

posts = soup.find_all("div", class_="x1lliihq")

print(f"👉 Kết quả: Tìm thấy {len(posts)} khối.")

# 4. IN THỬ NỘI DUNG ĐỂ KIỂM TRA
print("\n--- KIỂM TRA 3 KẾT QUẢ ĐẦU TIÊN ---")

count = 0
for post in posts:
    # Lấy text thô và xóa khoảng trắng thừa
    text = post.get_text(separator=" ", strip=True)
    
    # Chỉ in những khối có nội dung dài (để lọc bớt các div rác lồng nhau)
    if len(text) > 50: 
        count += 1
        print(f"\n[Khối {count}]:")
        print(text[:200] + "...") # Chỉ in 200 ký tự đầu
        print("-" * 30)
        
        if count >= 3: break # Chỉ xem thử 3 cái