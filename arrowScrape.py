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
    '''
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chromeDriverPath = 'C:\\Users\\Yeshai.Mishal\\installs\\chromedriver.exe'
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromeDriverPath)
'''
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(url)
    return driver

url = 'https://www.arrow.com/'
master = {}  # 2D dict with all part info

'''with open(filepath) as f:
    parts = list(f)

for part in parts:
    part = part.strip('\n')
    part = part.strip()
    print(part)
    q_string = part
    url = base_url + dir1 + q_string
    '''
# connect to url and pull page source (HTML)
try:
    driver = connect_url(url)
    driver.find_element_by_name("q").clear()
    driver.find_element_by_name("q").send_keys("LT1763CS8-3#PBF")
    driver.find_element_by_xpath(
        "(.//*[normalize-space(text()) and normalize-space(.)='All Categories'])[1]/following::span[1]").click()
    bsObj = BeautifulSoup(driver.page_source, 'lxml')
    if len(bsObj) > 0:
        print('page source aquired!')
    else:
        print('page source appears blank!')
        pprint(bsObj)
except TimeoutException:
    print('timeout error.')
    driver.quit()

specTable = bsObj.find('',{'id':'Pdp-specifications'})
specItems = specTable.ul.findAll('li')
print('KEY | VALUE')
for specItem in specItems:
    specItem = specItem.findAll('div')
    key = specItem[0].get_text().strip()
    value = specItem[1].get_text().strip()
    print(key + ' | ' + value)
driver.quit()