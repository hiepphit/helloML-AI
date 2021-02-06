from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import os
import pandas as pd
from selenium import webdriver
from datetime import datetime
import time


########################## DEFINE #####################
url = "https://www.nocibe.fr"
initLinkList = "/parfum/parfum-homme/C-48168/NW-1039-categorie~parfum"
#######################################################


now = datetime.now()
current_time = now.strftime("%H_%M_%d_%m_%y")

abs_dir = os.path.dirname(__file__)
new_csv_path = abs_dir+'/men_nocibe'+current_time+'.csv'

options = Options()
options.add_argument("--headless")
names = []  # List to store name of the Product
types = []  # List to store type of the Product Brand
prices = []  # List to store price of the Product Brand
brands = []  # List to store name of the Product Brand
links = []  # List to store link of the Product
counts = []
count = 0
try:
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    link = url+initLinkList
    driver.get(link)
    driver.execute_script(
        "for(i = 0; i<22;i++){document.getElementsByClassName('pagine__more')[0].click();}")
    time.sleep(30)
    content = driver.page_source
    soup = BeautifulSoup(content)
    listProduct = soup.find('div', attrs={'class': 'pager-list stories-1'})
    for a in listProduct.findAll('a', attrs={'class': 'gtmEventClick product-item product-item__after-story'}):
        tag = a
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
        header = productSoup.find(
            'h1', attrs={'class': 'prdct__maintitle'}).findAll('div')

        productName = header[1]
        if productName:
            names.append(productName.text)
        else:
            continue

        contentPrice = productSoup.find(
            'div', attrs={'class': 'prdct__pce-content'})
        price = 'null'
        if contentPrice:
            price = contentPrice.text
            price = price[1:]
        prices.append(price)

        descriptionName = header[2]
        if descriptionName:
            types.append(descriptionName.text)
        else:
            types.append('Not available')

        brandName = header[0]
        if brandName:
            brands.append(brandName.text)
        else:
            continue
        links.append(url+linkProduct)
        count += 1
        counts.append(count)
        print(count)
        driverProduct.close()
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
