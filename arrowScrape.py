# SINGLE RESULT: 02013A101JAT2A
# MULTIPLE RESULTS: 02013A1ROCAT2A

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
   # chrome_options.add_argument("--headless")
   # chrome_options.add_argument("--window-size=1920x1080")
   # chrome_options.add_argument("--proxy-server='direct://'");
   # chrome_options.add_argument("--proxy-bypass-list=*");
    chromeDriverPath = 'C:\\Users\\Yeshai.Mishal\\installs\\chromedriver.exe'
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromeDriverPath)
    #driver.minimize_window()
    # driver = webdriver.Chrome()
    driver.implicitly_wait(1)
    driver.get(url)
    return driver

url = 'https://www.arrow.com'
filepath = 'parts.txt'
master = {}  # 2D dict with all part info

with open(filepath) as f:
    parts = list(f)
    for part in parts:
        part = part.strip('\n')
        part = part.strip()
        print('PART: ' + part)
    # connect to url and pull page source (HTML)
        try:
            driver = connect_url(url)
            driver.find_element_by_name("q").clear()
            driver.find_element_by_name("q").send_keys(part)
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
        try:
            bsObj = BeautifulSoup(driver.page_source, 'lxml') #reload object for new page
            multipleResults = bsObj.find('h1',{'class':'SearchControls-heading SearchResultsCount'}) #results returned
            if not(multipleResults):
                print('multiple results = False')

                resultTable = bsObj.find('div', {'class': 'PartSpecifications'})
                # print('resultTable = ')
                # pprint(resultTable)
                partDict = {}
                if resultTable:
                    print('single result!')
                    specTable = bsObj.find('', {'id': 'Pdp-specifications'})
                    # print('specTable')
                    #pprint(specTable)
                    specItems = specTable.tbody.findAll('tr')
                    print('KEY | VALUE')
                    for specItem in specItems:
                        specItem = specItem.findAll('td', {'class':"col-sm-6"})
                        #print('specItem')
                        #pprint(specItem)
                        key = specItem[0].get_text().strip()
                        #print('key: ' + key)
                        value = specItem[1].get_text().strip()
                        #print('value: ' + value)
                        partDict[key] = value
                        print(key + ' | ' + value)
                        master[part] = partDict  # load part and properties into master dictionary

                        # write data to JSON file
                        with open('arrow_mult.json', 'w') as outfile:
                            json.dump(master, outfile, sort_keys=True, indent=4)

                    # read from JSON file
                    with open('arrow_mult.json') as data_file:
                       data = json.load(data_file)
                else:
                    driver.quit()
                    continue
            else:
                currentUrl = driver.current_url
                driver.quit()
                currentUrl += '&perPage=100'  # get 100 results per page
                driver = connect_url(currentUrl)

                # pprint(multipleResults)

                tableRow = bsObj.find('tr', {'id': 'item1'})
                # print('tableRow = ')
                # pprint(tableRow)
                tableRows = bsObj.findAll('tr', {
                    'class': 'SearchResults-resultRow SearchResults-productRow SearchResults-resultRow--eccn'})
                # print('tableRows = ')
                # pprint(tableRows)
                for tableRow in tableRows:
                    dataName = tableRow.attrs['data-name']  # part name
                    dataUrl = tableRow.attrs['data-part-url']  # part link
                    print('dataName = ' + dataName)
                    if dataName == part:
                        print('MATCH!')
                        print(dataName + ' = ' + part)
                        print('path = ' + dataUrl)
                        driver.quit()
                        part_url = url + dataUrl
                        driver = connect_url(part_url)
                        bsObj = BeautifulSoup(driver.page_source, 'lxml')  # reload object for new page
                        resultTable = bsObj.find('div', {'class': 'PartSpecifications'})
                        # print('resultTable = ')
                        # pprint(resultTable)
                        partDict = {}
                        if resultTable:
                            print('single result!')
                            specTable = bsObj.find('', {'id': 'Pdp-specifications'})
                            # print('specTable')
                            # pprint(specTable)
                            specItems = specTable.tbody.findAll('tr')
                            print('KEY | VALUE')
                            for specItem in specItems:
                                specItem = specItem.findAll('td', {'class': "col-sm-6"})
                                # print('specItem')
                                # pprint(specItem)
                                key = specItem[0].get_text().strip()
                                # print('key: ' + key)
                                value = specItem[1].get_text().strip()
                                # print('value: ' + value)
                                partDict[key] = value
                                print(key + ' | ' + value)
                                master[part] = partDict  # load part and properties into master dictionary

                                # write data to JSON file
                                with open('arrow_mult.json', 'w') as outfile:
                                    json.dump(master, outfile, sort_keys=True, indent=4)

                            # read from JSON file
                            with open('arrow_mult.json') as data_file:
                                data = json.load(data_file)
                    else:
                        driver.quit()
                        continue

        except TypeError:
            print('type errpor')

    pprint(master)
    driver.quit()