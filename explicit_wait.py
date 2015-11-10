from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.get("http://www.espncricinfo.com")
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "&lpos=headline_row1area2"))
    )
finally:
    driver.quit()
