# demo selenium
# #Test Selenium
from selenium import webdriver
import pandas as pd
import os
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
names = []  # List to store name of the Product
types = []  # List to store type of the Product Brand
prices = []  # List to store price of the Product Brand
brands = []  # List to store name of the Product Brand
links = []  # List to store link of the Product
counts = []
url = "https://www.notino.fr"
driver.get(url+"/parfums-homme/")

content = driver.page_source
soup = BeautifulSoup(content)
count = 0
try:
    for a in soup.findAll('li', attrs={'class': 'item-filtered'}):
        brand = a.find('a')
        brandLink = brand.attrs['href']
        driver1 = webdriver.Chrome(
            ChromeDriverManager().install(), options=options)
        driver1.get(url+brandLink)
        allProductSource = driver1.page_source
        if not allProductSource:
            continue
        allProductSoup = BeautifulSoup(allProductSource)
        for p in allProductSoup.findAll('li', attrs={'class': 'item'}):
            linkProduct = p.find('a').attrs['href']
            driverProduct = webdriver.Chrome(ChromeDriverManager().install(), options=options)
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
            contentPrice = productSoup.find('span', attrs={'class': 'styled__PriceWrapper-pp9c4m-1 fqeInH'})
            price = 'null'
            if contentPrice:
                price = contentPrice.find('span').attrs['content']
            
            names.append(productName)
            types.append(descriptionName)
            brands.append(brandName)
            links.append(url+linkProduct)
            prices.append(price)
            count +=1
            counts.append(count)
            print(count)
            print(productName)
            driverProduct.close()
        driver1.close()
    df = pd.DataFrame(
        {'No': counts, 'Name': names, 'Type': types, 'Brand Name': brands, 'Price': prices, 'Currency': 'EUR', 'Link': links})
    df.to_csv('full_men_notino.csv', index=False, encoding='utf-8')
except:
    df = pd.DataFrame(
        { 'No': counts, 'Name': names, 'Type': types, 'Brand Name': brands, 'Price': prices, 'Currency': 'EUR', 'Link': links})
    df.to_csv('full_men_notino.csv', index=False, encoding='utf-8')
