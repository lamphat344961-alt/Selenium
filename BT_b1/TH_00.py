from selenium import webdriver
from selenium.webdriver.common.by import By
import time
print("Hello world")

driver = webdriver.Chrome()

driver.get("https://gomotungkinh.com/")
time.sleep(10)
try :
    while True :
        driver.find_element(By.ID,"bonk").click()
        time.sleep(3)
except :
    driver.quit()