import time
import getpass
import pandas as pd  # Thêm thư viện này
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# 1. Cấu hình Chrome
chrome_options = Options()
chrome_options.add_argument("--disable-notifications") # Tắt thông báo
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

# 2. Đăng nhập
url = "https://www.facebook.com/"
driver.get(url)
time.sleep(2)

email = input("Nhập Email: ")
email_element = driver.find_element(By.ID, "email")
email_element.send_keys(email)

password = getpass.getpass("Nhập Mật khẩu: ")
pass_element = driver.find_element(By.ID, "pass")
pass_element.send_keys(password)
pass_element.send_keys(Keys.ENTER)

print("Đang đăng nhập... Vui lòng đợi 10 giây.")
time.sleep(10)

# 3. Cuộn trang (Tăng số lần range lên nếu muốn lấy nhiều bài hơn)
print("Đang cuộn trang...")
for i in range(5): 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

# 4. Thu thập dữ liệu
print("Đang xử lý dữ liệu...")
post_containers = driver.find_elements(By.XPATH, "//div[contains(@class, 'x1lliihq')]")
print(f"Tìm thấy {len(post_containers)} khối nội dung.")

# --- TẠO LIST ĐỂ CHỨA DỮ LIỆU ---
all_posts_data = []

for post in post_containers:
    try:
        # A. Người đăng (Dùng thuộc tính cố định data-ad-rendering-role)
        try:
            author_el = post.find_element(By.XPATH, ".//div[@data-ad-rendering-role='profile_name']")
            author = author_el.text
        except:
            author = "" # Nếu không tìm thấy tên thì bỏ qua hoặc để rỗng

        # Chỉ lấy dữ liệu nếu xác định được người đăng (lọc bỏ quảng cáo/rác)
        if author:
            # B. Nội dung (Dùng dir="auto" và style)
            try:
                content_el = post.find_element(By.XPATH, ".//*[@dir='auto'][contains(@style, 'text-align: start')]")
                content = content_el.text
            except:
                content = "Không có nội dung text"

            # C. Thống kê (Cảm xúc, Comment, Share)
            # Vào class cha x1n2onr6 -> tìm các class con x135b78x
            stats_list = []
            try:
                stat_items = post.find_elements(By.XPATH, ".//div[contains(@class, 'x1n2onr)] ")
                for item in stat_items:
                    txt = item.text
                    if txt: stats_list.append(txt)
            except:
                pass
            
            stats_str = ", ".join(stats_list) # Nối lại thành chuỗi: "500 Like, 20 Comment"

            # --- LƯU VÀO DICTIONARY ---
            post_item = {
                'Người đăng': author,
                'Nội dung': content,
                'Thống kê': stats_str
            }
            
            # Thêm vào danh sách tổng
            all_posts_data.append(post_item)
            
            # In ra màn hình để theo dõi tiến độ
            print(f"-> Đã lấy bài của: {author}")

    except Exception as e:
        print(f"Lỗi khi xử lý 1 bài viết: {e}")

# 5. Lưu ra Excel (Phần mới thêm)
if len(all_posts_data) > 0:
    df = pd.DataFrame(all_posts_data)
    
    # In xem trước
    print("\n--- KẾT QUẢ ---")
    print(df.head())
    
    file_name = 'Facebook_Data.xlsx'
    df.to_excel(file_name, index=False)
    print(f"\n✅ Đã lưu thành công vào file: {file_name}")
else:
    print("❌ Không thu thập được dữ liệu nào.")

driver.quit()