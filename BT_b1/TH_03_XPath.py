from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 1. Khởi tạo
driver = webdriver.Chrome()

# 2. Truy cập trang
url = r"https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22P%22"
driver.get(url)
time.sleep(5) # Chỉ cần 5s là đủ

# --- PHẦN SỬA ĐỔI QUAN TRỌNG ---

# Thay vì tìm mù quáng, ta dùng XPath để tìm thẳng vào nội dung chính (mw-content-text)
# Công thức: //div[@id='mw-content-text'] //li //a
# Ý nghĩa: Tìm div nội dung -> Vào trong tìm các dòng li -> Vào trong lấy thẻ a
print("Đang quét dữ liệu...")

# Lấy tất cả thẻ a nằm trong danh sách của phần nội dung chính
painter_links = driver.find_elements(By.XPATH, "//div[@id='mw-content-text']//div[contains(@class,'div-col')]//li//a")

# Nếu XPath trên không ra (do wiki đổi format), dùng cái tổng quát hơn này:
if len(painter_links) == 0:
    painter_links = driver.find_elements(By.XPATH, "//div[@id='mw-content-text']//ul//li//a")

print(f"Tìm thấy {len(painter_links)} họa sĩ.")

# --- XỬ LÝ VÀ IN KẾT QUẢ ---

# Chỉ lấy 10 người đầu tiên để test cho nhanh (bỏ [:10] nếu muốn lấy hết)
for tag in painter_links[:10]:
    name = tag.get_attribute("title")
    link = tag.get_attribute("href")
    

    print(f"Tên: {name} | Link: {link}")

driver.quit()