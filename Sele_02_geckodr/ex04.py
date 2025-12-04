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


# chờ ô username xuất hiện
email_element = WebDriverWait(driver,120).until(
    EC.presence_of_element_located((By.NAME, "username"))
)

email = 'FriendlyCharity9130'#input("Nhập Email: ")
email_element = driver.find_element(By.NAME, "username")
email_element.send_keys(email)

password = "dinhquockhanh8888" #getpass.getpass("Nhập Mật khẩu: ")
pass_element = driver.find_element(By.NAME, "password")
pass_element.send_keys(password)
pass_element.send_keys(Keys.ENTER)

time.sleep(10)



# # Truy cap trang post bai
url2 = 'https://www.reddit.com/user/dkasco/submit/?type=TEXT'
driver.get(url2)
time.sleep(5)
actionChains = ActionChains(driver)
for i in range(17):
    actionChains.key_down(Keys.TAB).perform()


actionChains.send_keys('Post tan phat').perform()


actionChains.key_down(Keys.TAB)
actionChains.key_down(Keys.TAB).perform()

actionChains.send_keys('123456').perform()

for i in range(2):
    actionChains.key_down(Keys.TAB).perform()
    time.sleep(3)

actionChains.send_keys(Keys.ENTER).perform()


time.sleep(120)
driver.quit()




