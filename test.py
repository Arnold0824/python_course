from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "http://localhost:5173//courses/python/ch07"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.get(f"{BASE_URL}/search_demo.html")
    search_box = wait.until(EC.presence_of_element_located((By.ID, "keyword")))
    search_box.clear()
    search_box.send_keys("Python")
    search_box.send_keys(Keys.ENTER)

    wait.until(lambda page: len(page.find_elements(By.CSS_SELECTOR, "#dynamicResults .product-card")) > 0)
    cards = driver.find_elements(By.CSS_SELECTOR, "#dynamicResults .product-card")
    for card in cards[:5]:
        title = card.find_element(By.CSS_SELECTOR, ".product-title").text
        price = card.find_element(By.CSS_SELECTOR, ".price strong").text
        print(title, price)
finally:
    driver.quit()