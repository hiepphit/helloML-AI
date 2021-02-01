# demo selenium
# #Test Selenium
from selenium import webdriver
import pandas as pd
import os
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
driver = webdriver.Chrome(ChromeDriverManager().install())
brands = []  # List to store name of the brand
links = []  # List to store link of the brand
quantities = []  # List to store quantity of the brand
driver.get("https://www.notino.fr/parfums-homme/")

content = driver.page_source
soup = BeautifulSoup(content)
count = 0
for a in soup.findAll('li', attrs={'class': 'item-filtered'}):
    quantity = a.find('span', attrs={'class': 'count'}).text
    quantities.append(quantity)
    brand = a.find('a')
    name = brand.attrs['title']
    brands.append(name)
    link = brand.attrs['href']
    links.append(link)
    count +=1
    print(count)
df = pd.DataFrame(
    {'Brand Name': brands, 'Quantities': quantities, 'Link': links})
df.to_csv('products_notino.csv', index=False, encoding='utf-8')
