from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import os
import pandas as pd
from selenium import webdriver
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H_%M_%d_%m_%y")

abs_dir = os.path.dirname(__file__)
new_csv_path = abs_dir+'/full_men_notino'+current_time+'.csv'

options = Options()
options.add_argument("--headless")
names = []  # List to store name of the Product
types = []  # List to store type of the Product Brand
prices = []  # List to store price of the Product Brand
brands = []  # List to store name of the Product Brand
links = []  # List to store link of the Product
counts = []
url = "https://www.notino.fr"

count = 0


try:
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url+"/parfums-homme/")
    content = driver.page_source
    soup = BeautifulSoup(content)
    while True:
        listProduct = soup.find('ul', attrs={'id': 'productsList'})
        for a in listProduct.findAll('li', attrs={'class': 'item'}):
            tag = a.find('a')
            if not tag:
                continue
            linkProduct = tag.attrs['href']
            driverProduct = webdriver.Chrome(
                ChromeDriverManager().install(), options=options)
            driverProduct.get(url+linkProduct)
            productSource = driverProduct.page_source
            if not productSource:
                continue
            productSoup = BeautifulSoup(productSource)
            header = productSoup.find('div', attrs={'id': 'pdHeader'})
            contentHeader = header.find('h1').findAll('span')
            brandName = contentHeader[0].text
            productName = contentHeader[1].text
            descriptionName = contentHeader[2].text
            contentPrice = productSoup.find(
                'span', attrs={'class': 'styled__PriceWrapper-pp9c4m-1 fqeInH'})
            price = 'null'
            if contentPrice:
                price = contentPrice.find('span').attrs['content']

            names.append(productName)
            types.append(descriptionName)
            brands.append(brandName)
            links.append(url+linkProduct)
            prices.append(price)
            count += 1
            counts.append(count)
            print(count)
            print(productName)
            driverProduct.close()
        nextE = soup.find('a', attrs={'class': 'next'})
        if nextE:
            nextPage = nextE.attrs['href']
            driver.get(nextPage)
            content = driver.page_source
            soup = BeautifulSoup(content)
        else:
            break
    driver.close()
    end = datetime.now()
    end_time = end.strftime("%H_%M_%d_%m_%y")
    print('END ==================== ' + end_time)
    df = pd.DataFrame(
        {'No': counts, 'Name': names, 'Type': types, 'Brand Name': brands, 'Price': prices, 'Currency': 'EUR', 'Link': links})
    df.to_csv(new_csv_path, index=False, encoding='utf-8')
except:
    end = datetime.now()
    end_time = end.strftime("%H_%M_%d_%m_%y")
    print('END ==================== ' + end_time)
    if len(names) > 0:
        df = pd.DataFrame(
            {'No': counts, 'Name': names, 'Type': types, 'Brand Name': brands, 'Price': prices, 'Currency': 'EUR', 'Link': links})
        df.to_csv(new_csv_path, index=False, encoding='utf-8')
