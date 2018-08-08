from bs4 import BeautifulSoup, element
import re
import sys
import json
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

def connect_url(url):
    # instantiate a chrome options object so you can set the size and headless preference
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chromeDriverPath = 'C:\\Users\\Yeshai.Mishal\\installs\\chromedriver.exe'
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromeDriverPath)

    #driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(url)
    return driver

base_url = 'https://www.digikey.com'
dir1 = '/products/en?keywords='
filepath = 'parts.txt'
master = {}  # 2D dict with all part info

with open(filepath) as f:
    parts = list(f)

for part in parts:
    part = part.strip('\n')
    part = part.strip()
    print(part)
    q_string = part
    url = base_url + dir1 + q_string
    # connect to url and pull page source (HTML)
    try:
        driver = connect_url(url)
        bsObj = BeautifulSoup(driver.page_source, 'lxml')
        if len(bsObj) > 0:
            print('page source aquired!')
        else:
            print('page source appears blank!')
            pprint(bsObj)
    except TimeoutException:
        print('timeout error.')
        driver.quit()
