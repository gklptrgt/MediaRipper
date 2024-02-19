from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

main_link = "https://aniwave.to/watch/one-piece.ov8/ep-1"
driver = webdriver.Chrome()

driver.get(main_link)

time.sleep(10)
soup = BeautifulSoup(driver.page_source, "lxml")

x = soup.select("#w-servers")
print(x)
