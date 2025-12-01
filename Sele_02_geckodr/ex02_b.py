from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException

# 1. Khởi tạo Firefox Driver
driver = webdriver.Firefox()

# --- SỬA ĐỔI: TRUY CẬP TRỰC TIẾP LINK TẤT CẢ SẢN PHẨM ---
url = "https://gochek.vn/collections/all" 
driver.get(url)

print("Đang truy cập trang danh sách sản phẩm...")
# Đợi trang tải xong (Dữ liệu sản phẩm cần thời gian để render)
time.sleep(8)


try:
    # Lấy danh sách tất cả các khối sản phẩm
    # XPath này tìm tất cả thẻ div có class chứa 'product-block'
    product_blocks = driver.find_elements(By.XPATH, "//div[contains(@class, 'product-block')]")
    
    print(f"🔍 Tìm thấy {len(product_blocks)} sản phẩm. Đang xử lý...")
    
    data_list = []

    for product in product_blocks:
        item = {}
        
        # A. Tên sản phẩm
        try:
            name_el = product.find_element(By.XPATH, ".//h3[contains(@class, 'pro-name')]/a")
            item['Tên sản phẩm'] = name_el.text
        except:
            item['Tên sản phẩm'] = ""

        # B. Giá hiện tại
        try:
            current_price_el = product.find_element(By.XPATH, ".//p[contains(@class, 'pro-price')]/span")
            item['Giá hiện tại'] = current_price_el.text
        except:
            item['Giá hiện tại'] = ""

        # --- C. Lấy Giá đang giảm (Giá gốc/Giá gạch ngang) ---
        try:
            old_price_el = product.find_element(By.XPATH, ".//span[contains(@class, 'pro-price-del')]//del")
            item['Giá gốc'] = old_price_el.get_attribute("textContent").strip()
        except:
            item['Giá gốc'] = ""     
    

        # D. Giảm giá
        try:
            # Tìm thẻ div chứa thông tin giảm giá
            discount_el = product.find_element(By.XPATH, ".//div[contains(@class, 'product-sale')]")
            item['Giảm giá'] = discount_el.text.replace("-", "").strip()
        except:
            item['Giảm giá'] = ""

        # E. Link ảnh (Xử lý kỹ lazy load)
        try:
            img_el = product.find_element(By.TAG_NAME, "img")
            
            # Ưu tiên lấy data-src (ảnh thật) trước, nếu không có mới lấy src
            src = img_el.get_attribute('data-src')
            if not src:
                src = img_el.get_attribute('src')
            
            # Xử lý link thiếu https (thường gặp ở web Haravan/Sapo)
            if src and src.startswith("//"):
                src = "https:" + src
                
            item['Link ảnh'] = src
        except:
            item['Link ảnh'] = ""

        # F. Trạng thái (Hết hàng/Còn hàng)
        try:
            sold_out_flags = product.find_elements(By.XPATH, ".//*[contains(@class, 'sold-out')]")
            if len(sold_out_flags) > 0:
                item['Trạng thái'] = "Hết hàng"
            else:
                item['Trạng thái'] = "Còn hàng"
        except:
            item['Trạng thái'] = "Còn hàng"

        data_list.append(item)

    # 4. Xuất ra Excel
    if data_list:
        df = pd.DataFrame(data_list)
        
        # Sắp xếp thứ tự cột
        cols = ['Tên sản phẩm', 'Giá hiện tại', 'Giá gốc', 'Giảm giá', 'Trạng thái', 'Link ảnh']
        # Chỉ lấy các cột có trong dữ liệu
        final_cols = [c for c in cols if c in df.columns]
        df = df[final_cols]
        
        print("\n--- KẾT QUẢ MẪU ---")
        print(df.head())
        
        excel_name = r"C:\Users\Admin\Desktop\TANPHAT\Manguonmotrongkhoahocjdulieu\Selenium\Sele_02_geckodr\Danh_sach_san_pham_Gochek.xlsx"
        df.to_excel(excel_name, index=False)
        print(f"\n✅ Đã lưu thành công file: {excel_name}")
    else:
        print("❌ Không lấy được dữ liệu nào.")

except Exception as e:
    print(f"❌ Có lỗi xảy ra: {e}")

finally:
    driver.quit()