from selenium import webdriver
from selenium.webdriver.common.by import By
from pygments.formatters.html import webify 
import time

driver = webdriver.Chrome()

url = r"https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22P%22"
driver.get(url)
# driver.maximize_window()
time.sleep(10)

ul_tags = driver.find_elements(By.TAG_NAME, "ul") 
print(len(ul_tags))

links = [tag.get_attribute("href") for tag in ul_tags ]

ul_painters = ul_tags[20]

li_tags = ul_painters.find_elements(By.TAG_NAME, "li")

links = [tag.find_element(By.TAG_NAME, 'a').get_attribute("href") for tag in li_tags ]

titles = [tag.find_element(By.TAG_NAME, 'a').get_attribute("title") for tag in li_tags ]

for link in links:
    print(link)

for title in titles:
    print(title)


driver.quit()