from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# ================== HÀM LẤY THÔNG TIN TRONG INFOBOX ==================
def scrape_infobox_on_current_page(driver):
    """
    Lấy các thông tin trong infobox (nếu có):
    - Hiệu trưởng
    - Thành lập
    - Loại
    - Thành viên của
    """
    result = {
        "Hiệu trưởng": "",
        "Thành lập": "",
        "Loại": "",
        "Thành viên của": ""
    }

    try:
        # đợi bảng infobox xuất hiện nếu có
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "table.infobox")
            )
        )
    except:
        # không có infobox
        return result

    label_map = {
        "Hiệu trưởng": "Hiệu trưởng",
        "Thành lập": "Thành lập",
        "Loại": "Loại",
        "Thành viên của": "Thành viên của"
    }

    for label_text, key in label_map.items():
        try:
            td = driver.find_element(
                By.XPATH,
                "//table[contains(@class,'infobox')]"
                "//tr[th[contains(@class,'infobox-label') and contains(normalize-space(), '{}')]]"
                "/td".format(label_text)
            )
            result[key] = td.text.strip()
        except:
            # không có dòng tương ứng thì để rỗng
            pass

    return result


# ================== CẤU HÌNH SELENIUM ==================
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

url = "https://vi.wikipedia.org/wiki/Danh_s%C3%A1ch_tr%C6%B0%E1%BB%9Dng_%C4%91%E1%BA%A1i_h%E1%BB%8Dc,_h%E1%BB%8Dc_vi%E1%BB%87n_v%C3%A0_cao_%C4%91%E1%BA%B3ng_t%E1%BA%A1i_Vi%E1%BB%87t_Nam"

driver.get(url)
time.sleep(3)  # chờ trang load

main_window = driver.current_window_handle  # lưu lại tab chính

# ================== TÌM TẤT CẢ CÁC BẢNG WIKITABLE ==================
tables = driver.find_elements(By.CSS_SELECTOR, "table.wikitable")
print(f"Tìm thấy {len(tables)} bảng 'wikitable'.")

for idx, table in enumerate(tables, start=1):
    print(f"\nĐang xử lý bảng {idx} ...")

    # ----- 1. Lấy header -----
    headers = []
    try:
        header_row = table.find_element(By.TAG_NAME, "thead") \
                           .find_element(By.TAG_NAME, "tr")
        header_cells = header_row.find_elements(By.TAG_NAME, "th")
        headers = [h.text.strip() for h in header_cells]
    except:
        # Một số bảng không có thead, header nằm ở tr đầu tiên của tbody
        tbody = table.find_element(By.TAG_NAME, "tbody")
        first_row = tbody.find_elements(By.TAG_NAME, "tr")[0]
        header_cells = first_row.find_elements(By.TAG_NAME, "th")
        headers = [h.text.strip() for h in header_cells]

    print("Header:", headers)

    # Thêm 4 cột extra
    extra_cols = ["Hiệu trưởng", "Thành lập", "Loại", "Thành viên của"]

    # ----- 2. Lấy dữ liệu từng dòng -----
    data_rows = []
    tbody = table.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")

    for r_idx, r in enumerate(rows, start=1):
        tds = r.find_elements(By.TAG_NAME, "td")
        if not tds:
            continue

        row_data = [td.text.strip() for td in tds]

        if len(row_data) < len(headers):
            row_data += [""] * (len(headers) - len(row_data))

        row_data = row_data[:len(headers)]

        row_dict = {headers[i]: row_data[i] for i in range(len(headers))}

        detail_url = ""
        try:
            link_el = r.find_element(By.XPATH, ".//a[starts-with(@href, '/wiki/')]")
            detail_url = link_el.get_attribute("href")
        except:
            detail_url = ""

        # mặc định 4 cột extra rỗng
        for c in extra_cols:
            row_dict[c] = ""

        # Nếu có link thì mở tab mới để crawl infobox
        if detail_url:
            print(f"  [Bảng {idx} - Dòng {r_idx}] Vào: {detail_url}")
            try:
                # mở tab mới
                driver.switch_to.new_window('tab')
                driver.get(detail_url)
                time.sleep(1.5)

                info = scrape_infobox_on_current_page(driver)

                # ghi lại vào row_dict
                for c in extra_cols:
                    row_dict[c] = info.get(c, "")

            except Exception as e:
                print(f"    Lỗi khi crawl infobox: {e}")
            finally:
                # đóng tab hiện tại và quay lại tab chính
                driver.close()
                driver.switch_to.window(main_window)

        data_rows.append(row_dict)

    # ----- 3. Đưa vào DataFrame + Lưu CSV (KHÔNG GỘP) -----
    if data_rows:
        df = pd.DataFrame(data_rows)
        filename = f"wiki_bang_{idx}.csv"
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"✅ Đã lưu bảng {idx} -> {filename}")
    else:
        print(f"⚠ Bảng {idx} không có dữ liệu td nào, bỏ qua.")

driver.quit()
