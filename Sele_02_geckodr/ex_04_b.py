import time
import getpass
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# 1. Cấu hình Chrome
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")   # Tắt popup noti
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

# 2. Đăng nhập Facebook
url = "https://www.facebook.com/"
driver.get(url)
time.sleep(2)

email = 'lamtrantanphat2005@gmail.com'
email_element = driver.find_element(By.ID, "email")
email_element.send_keys(email)

password = '0979344961'  #getpass.getpass("Nhập Mật khẩu: ")
pass_element = driver.find_element(By.ID, "pass")
pass_element.send_keys(password)
pass_element.send_keys(Keys.ENTER)

print("Đang đăng nhập... Vui lòng đợi 10 giây.")
time.sleep(10)

# 3. Cuộn trang để load nhiều bài hơn
print("Đang cuộn trang...")
for i in range(1):   # tăng số lần range nếu muốn lấy nhiều bài hơn
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

# 4. Thu thập dữ liệu
print("Đang xử lý dữ liệu...")

# MỖI BÀI POST: <div ... data-ad-preview="message">
post_containers = driver.find_elements(By.XPATH, "//div[@data-ad-preview='message']")
print(f"Tìm thấy {len(post_containers)} bài post.")

all_posts_data = []

for post in post_containers:
    try:
        # A. Người đăng
        try:
            author_el = post.find_element(
                By.XPATH, ".//*[@data-ad-rendering-role='profile_name']"
            )
            author = author_el.text.strip()
        except:
            author = ""

        # Bỏ qua nếu không xác định được người đăng
        if not author:
            continue

        # B. Nội dung bài viết (text chính)
        try:
            content_el = post.find_element(
                By.XPATH,
                ".//div[@dir='auto' and contains(@style, 'text-align: start')]"
            )
            content = content_el.text.strip()
            if not content:
                content = "Không có nội dung text"
        except:
            content = "Không có nội dung text"

        # C. Thống kê (Cảm xúc, Bình luận, Chia sẻ)
        reactions = ""
        comments = ""
        shares = ""

        try:
            # 1) Từ text "Xem ai đã bày tỏ cảm xúc về tin này"
            #    đi lên khối cha chứa toàn bộ thống kê
            stats_root = post.find_element(
                By.XPATH,
                ".//span[contains(@aria-label, 'Xem ai đã bày tỏ cảm xúc về tin này')]/ancestor::div[1]"
            )

            # 2) Lấy số CẢM XÚC
            #    Thường số like nằm trong <span> ngay trước nút "Tất cả cảm xúc"
            try:
                reaction_count_el = stats_root.find_element(
                    By.XPATH,
                    ".//div[normalize-space()='Tất cả cảm xúc']/preceding::span[@dir='auto'][1]"
                )
                reactions = reaction_count_el.text.strip()
            except:
                reactions = ""

            # 3) Lấy BÌNH LUẬN (span chứa chữ "Bình luận")
            try:
                comment_el = stats_root.find_element(
                    By.XPATH,
                    ".//span[@dir='auto'][contains(., 'Bình luận')]"
                )
                comments = comment_el.text.strip()
            except:
                comments = ""

            # 4) Lấy CHIA SẺ (span chứa chữ "chia sẻ" / "Chia sẻ")
            try:
                share_el = stats_root.find_element(
                    By.XPATH,
                    ".//span[@dir='auto'][contains(translate(., 'CS', 'cs'), 'chia sẻ')]"
                )
                shares = share_el.text.strip()
            except:
                shares = ""

        except Exception as e:
            # Không tìm được khối thống kê cho post này → để trống
            reactions = ""
            comments = ""
            shares = ""
        post_item = {
            'Người đăng': author,
            'Nội dung': content,
            'Cảm xúc': reactions,
            'Bình luận': comments,
            'Chia sẻ': shares,

        }
        all_posts_data.append(post_item)

        print(f"-> Đã lấy bài của: {author}")

    except Exception as e:
        print(f"Lỗi khi xử lý 1 bài viết: {e}")

# 5. Lưu ra Excel
if all_posts_data:
    df = pd.DataFrame(all_posts_data)

    print("\n--- KẾT QUẢ MẪU ---")
    print(df.head())

    file_name = r"C:\Users\Admin\Desktop\TANPHAT\Manguonmotrongkhoahocjdulieu\Selenium\Sele_02_geckodr\Facebook_Data.xlsx"
    df.to_excel(file_name, index=False)
    print(f"\n✅ Đã lưu thành công vào file: {file_name}")
else:
    print("❌ Không thu thập được dữ liệu nào.")

driver.quit()
