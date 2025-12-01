from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
import time
import pandas as pd
import getpass

driver = webdriver.Chrome()

# Tạo url
url = 'https://www.reddit.com/login/'

# Truy cập
driver.get(url)
time.sleep(10)

email = 'dkasco'#input("Nhập Email: ")
email_element = driver.find_element(By.NAME, "username")
email_element.send_keys(email)

password = "dinhquockhanh8888" #getpass.getpass("Nhập Mật khẩu: ")
pass_element = driver.find_element(By.NAME, "password")
pass_element.send_keys(password)
pass_element.send_keys(Keys.ENTER)

time.sleep(5)



# # Truy cap trang post bai
# url2 = 'https://www.reddit.com/user/tungit2024/submit/?type=TEXT'
# driver.get(url2);
# time.sleep(2)




time.sleep(120)
driver.quit()





