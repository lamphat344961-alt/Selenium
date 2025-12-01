import os
import time
import sqlite3
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

######################################################
# HÀM TÁCH CHUỖI DÒNG HỌA SĨ
######################################################

def parse_painter_line(line: str):
    """
    Ví dụ:
        'Gwilym Prichard (1931–2015) Welsh painter'
    Trả về:
        name, birth_year, death_year, nationality
    """
    line = line.strip().replace(',', '')
    n = len(line)
    i = 0

    # 1) Tên: chạy tới trước dấu '('
    while i < n and line[i] != '(':
        i += 1
    name = line[:i].strip()

    # Nếu không có '(' thì chỉ trả name, còn lại N/A
    if i == n:
        return name, "N/A", "N/A", "N/A"

    # 2) Năm sinh – mất: từ '(' đến ')'
    i += 1  # bỏ '('
    j = i
    while j < n and line[j] != ')':
        j += 1
    years_part = line[i:j].strip()   # ví dụ: '1931–2015'

    # Chuẩn hoá dấu gạch (có thể là '-' hoặc '–')
    years_norm = years_part.replace('–', '-')
    birth_year = "N/A"
    death_year = "N/A"
    if '-' in years_norm:
        parts = years_norm.split('-', 1)
        if parts[0].strip().isdigit():
            birth_year = parts[0].strip()
        if parts[1].strip().isdigit():
            death_year = parts[1].strip()

    # 3) Quốc tịch: sau dấu ')', bỏ khoảng trắng, đọc đến khoảng trắng đầu tiên
    j += 1  # bỏ ')'

    # bỏ các space sau ')'
    while j < n and line[j] == ' ':
        j += 1

    k = j
    while k < n and line[k] != ' ':
        k += 1

    nationality = line[j:k].strip() if j < n else "N/A"

    return name, birth_year, death_year, nationality

print(parse_painter_line("Gwilym Prichard (1931–2015) Welsh painter"))



######################################################
# I. SELENIUM – LẤY DỮ LIỆU TRONG LI
######################################################

driver = webdriver.Chrome()
all_data = []

print("\n--- BẮT ĐẦU QUÉT A–Z ---")

for i in range(65, 70):  # A–E để test; muốn full dùng range(65, 91)
    letter = chr(i)
    url = f'https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22{letter}%22'
    print(f"\nĐang xử lý chữ: {letter}")

    try:
        driver.get(url)
        time.sleep(2)

        # lấy tất cả li
        li_list = driver.find_elements(
            By.XPATH,
            "//div[@id='mw-content-text']//div[contains(@class,'div-col')]//li"
        )
        if len(li_list) == 0:
            li_list = driver.find_elements(By.XPATH, "//div[@id='mw-content-text']//ul/li")

        print(f"  -> Tìm thấy {len(li_list)} họa sĩ.")

        for li in li_list:
            try:
                full_text = li.text.strip()
                if not full_text:
                    continue

                # Lấy href từ thẻ <a>
                a = li.find_element(By.TAG_NAME, "a")
                href = a.get_attribute("href")

                # Dùng logic while để tách name, birth, death, nationality
                name, birth, death, nationality = parse_painter_line(full_text)

                # Lưu vào list
                all_data.append({
                    "Name": name,
                    "Birth": birth,
                    "Death": death,
                    "Nationality": nationality,
                    "Link": href
                })

            except Exception as e:
                print("  -> lỗi 1 li:", e)

    except Exception as e:
        print("  -> lỗi toàn trang:", e)


driver.quit()


######################################################
# II. XUẤT EXCEL
######################################################

if all_data:
    df = pd.DataFrame(all_data)
    df.to_excel("Painters_Final.xlsx", index=False)
    print("\nĐã lưu thành công vào Painters_Final.xlsx")
else:
    print("Không thu thập được dữ liệu nào.")
