from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import os
import pandas as pd
from selenium import webdriver
from datetime import datetime
import time

now = datetime.now()
current_time = now.strftime("%H_%M_%d_%m_%y")
options = Options()
# options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
names = []  # List to store name of the Product
types = []  # List to store type of the Product Brand
prices = []  # List to store price of the Product Brand
brands = []  # List to store name of the Product Brand
links = []  # List to store link of the Product
counts = []
url = "https://www.sephora.com"

count = 0
try:
    for i in range(6):
        link = url+"/shop/fragrances-for-men?currentPage="+str(i+1)
        driver.get(link)
        position = 0
        for b in range(5):
            position += 940
            driver.execute_script("window.scrollTo(0,"+str(position)+")")
            time.sleep(1)
        content = driver.page_source
        soup = BeautifulSoup(content)
        listProduct = soup.find('div', attrs={'data-comp': 'ProductGrid '})
        for a in listProduct.findAll('a', attrs={'class': 'css-ix8km1'}):
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
                'h1', attrs={'class': 'css-11zrkxf e65zztl0'})
            
            productName = header.find('span')
            if productName:
                names.append(productName.text)
            else:
                continue

            
            contentPrice = productSoup.find(
                'b', attrs={'class': 'css-0'})
            price = 'null'
            if contentPrice:
                price = contentPrice.text
                price = price[1:]
            prices.append(price)

            descriptionName = productSoup.find(
                'span', attrs={'class': 'css-15ro776'})
            if descriptionName:
                types.append(descriptionName.text)
            else:
                types.append('Not available')

            brandName = header.find('a')
            if brandName:
                brands.append(brandName.text)
            else:
                continue
            links.append(url+linkProduct)
            count += 1
            counts.append(count)
            print(count)
            driverProduct.close()
    end = datetime.now()
    end_time = end.strftime("%H_%M_%d_%m_%y")
    print('END ==================== '+ end_time)
    df = pd.DataFrame(
        {'No': counts, 'Name': names, 'Type': types, 'Brand Name': brands, 'Price': prices, 'Currency': 'USD', 'Link': links})
    df.to_csv('./perfume/Shephora/full_men_shephora'+current_time +
              '.csv', index=False, encoding='utf-8')
except:
    end = datetime.now()
    end_time = end.strftime("%H_%M_%d_%m_%y")
    print('END ==================== ' + end_time)
    if len(names) > 0:
        df = pd.DataFrame(
            {'No': counts, 'Name': names, 'Type': types, 'Brand Name': brands, 'Price': prices, 'Currency': 'USD', 'Link': links})
        df.to_csv('./perfume/Shephora/full_men_shephora'+current_time +
                '.csv', index=False, encoding='utf-8')
