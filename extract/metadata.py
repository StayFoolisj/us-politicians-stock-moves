from pprint import pprint
import random
import time
import uuid
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def getDriver(use_proxy=False, user_agent=None):

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(
        executable_path='/Users/ape/Desktop/black_magic/politicians_stock_movements/extract/chromedriver', options=options)
    return driver


def generate_transaction_id():
    return str(uuid.uuid4())


def view_more_results():
    show_option = driver.find_element_by_xpath(
        "/html/body/div[1]/main/div/div/div[6]/div/div/div/div[3]/div[1]/div/label/select")  # change value to '100'
    show_option.send_keys("100")
    show_option.send_keys(Keys.ENTER)
    time.sleep(1)  # Wait for the data to load


def get_doc_format(url):
    if any(word in url for word in ('paper',)):
        return 'paper'
    return 'electronic'


def specify_date_range(from_date, to_date):
    driver.find_element_by_id("fromDate").send_keys(from_date)
    driver.find_element_by_id("toDate").send_keys(to_date)
    time.sleep(0.4)


def extract_doc_table_data(row, column):
    if column == 4:
        return driver.find_element_by_xpath(f"/html/body/div[1]/main/div/div/div[6]/div/div/div/table/tbody/tr[{str(row)}]/td[4]/a").get_attribute('href')

    return driver.find_element_by_xpath(f"/html/body/div[1]/main/div/div/div[6]/div/div/div/table/tbody/tr[{str(row)}]/td[{str(column)}]").text


def pass_agreement_form(driver):
    # Click the first-page checkbox
    driver.get('https://efdsearch.senate.gov/')
    driver.find_element_by_id("agree_statement").click()
    time.sleep(1)

# Instantiating our driver
driver = getDriver()

database = {}
electronic = {}
paper = {}


def extract(from_date, to_date):

    count = 0
    time.sleep(1)

    # Click the first-page checkbox
    pass_agreement_form(driver)


    # Selecting Senator, Candidate and Former Senator
    for checkbox in driver.find_elements_by_id("filerTypes"):
        time.sleep(0.2)
        checkbox.click()
    time.sleep(0.2)

    # Selecting Periodic Transactions
    for checkbox in driver.find_elements_by_id("reportTypes"):
        if checkbox.get_attribute('value') == '11':
            checkbox.click()

    # Adding the desired date range
    specify_date_range(from_date, to_date)

    # Proceeding to the search results
    date = driver.find_element_by_id("toDate")
    date.send_keys(Keys.ENTER)
    date.send_keys(Keys.ENTER)  # Needed bec reasons
    time.sleep(1)

    row_count = len(driver.find_elements_by_xpath('/html/body/div[1]/main/div/div/div[6]/div/div/div/table/tbody/tr'))
    column_count = len(driver.find_elements_by_xpath('/html/body/div[1]/main/div/div/div[6]/div/div/div/table/tbody/tr[1]/td'))
    
    # Expanding results from 25 -> 100
    if row_count >= 25:
        view_more_results()
        row_count = len(driver.find_elements_by_xpath(
            '/html/body/div[1]/main/div/div/div[6]/div/div/div/table/tbody/tr'))
        #assert (row_count > 25), "Row count is still the same!"
    #print(row_count)

    if row_count > 0:
        # Iterating over the datatable
        for row in range(1, row_count+1):
            count += 1

            transaction_id = generate_transaction_id()

            row_data = [extract_doc_table_data(row, x) for x in range(1, 6)]
            first_name, last_name, office, url, filing_date = row_data
            #print(first_name)

            entry = {
                'url': url,
                "first_name": first_name,
                "last_name": last_name,
                "office": office,
                "filing_date": filing_date
            }

            # Reports will display in the format they were filed: either electronically (text) or on paper (images).
            if get_doc_format(url) == 'electronic':
                electronic[transaction_id] = entry

            else:
                paper[transaction_id] = entry

        driver.delete_all_cookies()
        driver.quit()
        print(f"Found {row_count} documents! Storing them all for further analysis")
        print(f"{len(electronic)} Electronic records: ")
        print(F"{len(paper)} Paper records:")
        return electronic, paper
    else:
        print("No documents found!")
        driver.delete_all_cookies()
        driver.quit()
        pass


# Uncomment to run
#collect_metadata('01/01/2020', '01/30/2020')
