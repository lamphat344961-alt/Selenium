from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Khởi tạo Webdriver
driver = webdriver.Chrome()

# Chạy vòng lặp từ mã ASCII 65 (A) đến 90 (Z)
# range(65, 91) nghĩa là chạy đến 90 thì dừng
for i in range(65, 91):
    # Tạo URL theo ký tự A, B, C...
    # chr(i) chuyển số thành chữ cái
    url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22" + chr(i) + "%22"
    titles = []
    
    try:
        # Mở trang
        driver.get(url)
        
        # Đợi một chút để trang tải
        time.sleep(3)
             
        painter_links = driver.find_elements(By.XPATH, "//div[@id='mw-content-text']//div[contains(@class,'div-col')]//li//a")

        for tag in painter_links[:5]:
            name = tag.get_attribute("title")
    
        # Tao danh sach cac title (tên họa sĩ)
            titles.append(name)
        
        for title in titles:
            print(title)


    except Exception as e:
        # In lỗi cụ thể để biết sai ở đâu thay vì chỉ in "Error!"
        print(f"Error at letter {chr(i)}: {e}")

# Dong webdriver
driver.quit()