from pprint import pprint
import pandas as pd
import requests
import random
import time
import uuid
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import metadata

DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_unique_id():
    return str(uuid.uuid4())

def dict_to_csv(dict):
    new_list = []

    def dict_to_list(dict):
        for key in dict:
            entry = [
                key,
                dict[key]['first_name'],
                dict[key]['last_name'],
                dict[key]['office'],
                dict[key]['filing_date'],
                dict[key]['url']
            ]
            new_list.append(entry)
        return new_list

    def list_to_dataframe(list):
        df = pd.DataFrame(new_list)
        df.columns = ['id', 'first_name', 'last_name', 'office', 'filing_date', 'url']
        return df

    def dataframe_to_csv(df):
        df.to_csv(F'{BASE_DIR}/extract/documents/{generate_unique_id()}.csv', index=True, header=True)

    dataframe_to_csv(list_to_dataframe(dict_to_list(dict)))


def getDriver(use_proxy=False, user_agent=None):

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(
        executable_path='/Users/ape/Desktop/black_magic/politicians_stock_movements/extract/chromedriver', 
        options=options
        )
    return driver


def extract_transaction_table_data(row, column):
    return driver.find_element_by_xpath(f"/html/body/div/main/div/div/section/div/div/table/tbody/tr[{str(row)}]/td[{str(column)}]").text


def extract_document_id(url):
    url = url[:-1]
    return url.rsplit('/', 1)[-1]


def post_to_API(id, data):
    r = requests.post(url=F"http://127.0.0.1:5000/transaction/{id}", json=data)
    return r.text

# Instantiating our driver
driver = getDriver()

def extract(from_date, to_date):
    
    # First we extract the metadata containing the lower level document data
    meta_electronic, meta_paper = metadata.extract(from_date, to_date)
    electronic_docs_amount, paper_docs_amount = len(meta_electronic), len(meta_paper)

    # As we need to manually process the paper documents, we save them in a csv file for later
    if paper_docs_amount != 0:
        dict_to_csv(meta_paper)
        print(F"Saved {paper_docs_amount} paper documents for manual extraction..")
        meta_paper.clear()

    if electronic_docs_amount == 0:
        print('quitting')
        return

    time.sleep(1)

    metadata.pass_agreement_form(driver)
    time.sleep(1)
    print(F"Commencing extraction of {electronic_docs_amount} electronic documents..")

    # Iterating our metadata to extract documents
    for n in meta_electronic:
        count = 0
        driver.get(meta_electronic[n]['url'])
        time.sleep(1)

        row_count = len(driver.find_elements_by_xpath('/html/body/div/main/div/div/section/div/div/table/tbody/tr'))
        column_count = len(driver.find_elements_by_xpath('/html/body/div/main/div/div/section/div/div/table/tbody/tr[1]/td'))

        if DEBUG:
            print(
                F"{meta_electronic[n]['first_name']} {meta_electronic[n]['last_name']} has {row_count} transactions. Initiating document extraction now")

        # Iterating over the datatable
        for row in range(1, row_count+1):
            count += 1
            #print(count)
            row_data = [extract_transaction_table_data(
                row, x) for x in range(1, column_count+1)]

            _, transaction_date, owner, ticker, asset_name, asset_type, transaction_type, amount, comment = row_data
            transaction_id = generate_unique_id()

            transaction = {
                "asset_name": asset_name,
                "asset_type": asset_type,
                "ticker": ticker,
                "owner": owner,
                "transaction_type": transaction_type,
                "transaction_date": transaction_date,
                "amount": amount,
                "comment": comment,
                "document_id": extract_document_id(meta_electronic[n]['url']),
                "document_url": meta_electronic[n]['url'],
                "document_type": driver.find_element_by_xpath('/html/body/div/main/div/div/div[2]/div[1]/h1').text,
                "filing_date": driver.find_element_by_xpath("/html/body/div/main/div/div/div[2]/div[1]/p/strong").text,
            }

            # Adding the transaction dict to the metadata and posting it to the API
            meta_electronic[n].update(transaction)
            post_to_API(transaction_id, meta_electronic[n])


    if DEBUG:
        print(F"Found {len(meta_electronic)} records in total")
        print(F"The length of meta_electronic is {len(meta_electronic.keys())}")

# Iterating through our dict and posting to database
#keys = [post_to_API(x, meta_electronic[x]) for x in meta_electronic.keys()]
# execute = [main(from_date, to_date) for from_date, to_date in dates.keys()]

