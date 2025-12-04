import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys # Cần thêm thư viện này để dùng Keys.ENTER

# --- CẤU HÌNH ---
REDDIT_USERNAME = "FriendlyCharity9130"  
REDDIT_PASSWORD = "dinhquockhanh8888" 
TARGET_SUBREDDIT = "https://www.reddit.com/r/PokemonTGCP/" 
SCROLL_TIMES = 5 

def crawl_subreddit_data(driver, url):
    """Crawl dữ liệu dựa trên phân tích thẻ <shreddit-post>"""
    print(f"🚀 Đang truy cập subreddit: {url}")
    driver.get(url)
    time.sleep(5) 

    # --- KỸ THUẬT INFINITE SCROLL ---
    print(f"⬇️ Bắt đầu cuộn trang {SCROLL_TIMES} lần...")
    for i in range(SCROLL_TIMES):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"   Đã cuộn lần {i+1}/{SCROLL_TIMES} - Chờ load dữ liệu...")
        time.sleep(4) 

    # --- TRÍCH XUẤT DỮ LIỆU ---
    print("🔍 Đang quét các thẻ <shreddit-post>...")
    posts = driver.find_elements(By.TAG_NAME, "shreddit-post")
    
    data_list = []
    
    for post in posts:
        try:
            item = {
                'title': post.get_attribute("post-title"),
                'score': post.get_attribute("score"),
                'author': post.get_attribute("author"),
                'subreddit': post.get_attribute("subreddit-prefixed-name"),
                'created_at': post.get_attribute("created-timestamp"),
                'comment_count': post.get_attribute("comment-count"),
                'post_type': post.get_attribute("post-type"),
                'permalink': "https://www.reddit.com" + post.get_attribute("permalink") if post.get_attribute("permalink") else None
            }
            
            if item['author'] and item['title']:
                data_list.append(item)
                
        except Exception as e:
            print(f"⚠️ Lỗi khi parse một post: {e}")
            continue

    return data_list

def save_to_csv(data):
    if not data:
        print("❌ Không thu thập được dữ liệu nào.")
        return

    df = pd.DataFrame(data)
    
    try:
        df['created_at'] = pd.to_datetime(df['created_at'])
    except:
        pass

    filename = "reddit_data.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"✅ Đã lưu {len(df)} dòng dữ liệu vào file '{filename}'")
    print(df.head())

# --- MAIN ---
if __name__ == "__main__":
    # 1. Khởi tạo Driver cơ bản theo yêu cầu
    print("🔄 Khởi tạo Chrome Driver...")
    driver = webdriver.Chrome()

    try:
        # 2. Quy trình đăng nhập mới
        url_login = 'https://www.reddit.com/login/'
        print("🔑 Đang truy cập trang đăng nhập...")
        driver.get(url_login)

        # Chờ ô username xuất hiện
        email_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        print(f"✍️ Nhập username: {REDDIT_USERNAME}")
        email_element.send_keys(REDDIT_USERNAME)

        print("✍️ Nhập password...")
        pass_element = driver.find_element(By.NAME, "password")
        pass_element.send_keys(REDDIT_PASSWORD)
        
        print("🖱️ Nhấn Enter để đăng nhập...")
        pass_element.send_keys(Keys.ENTER)

        print("⏳ Chờ 10s để chuyển hướng...")
        time.sleep(10)

        # 3. Tiến hành Crawl
        data = crawl_subreddit_data(driver, TARGET_SUBREDDIT)
        
        # 4. Lưu dữ liệu
        save_to_csv(data)
        
    except Exception as e:
        print(f"❌ Có lỗi xảy ra: {e}")
        
    finally:
        print("🛑 Đóng trình duyệt.")
        driver.quit()