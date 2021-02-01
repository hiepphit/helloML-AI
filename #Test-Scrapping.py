


#New reference viblo
# in crawler folder



#Using Requests Library
import requests
from bs4 import BeautifulSoup
import pandas as pd

products = []  # List to store name of the product
prices = []  # List to store price of the product
brands = []  # List to store brand of the product
links = []  # List to store detail link of the product
count = 0
for i in range(7):
    response = requests.get(
        "https://www.thegioinuochoa.com.vn/nuoc-hoa-ban-chay/#", params={"sex": 146, "page": int(i+1), "bestseller": 1})
    soup = BeautifulSoup(response.content, "html.parser")
    body = soup.findAll('div', class_='product-item-body')
    if len(body) > 0:
        for item in body:
            name = item.find('a', class_='product-name').text
            link = "https://www.thegioinuochoa.com.vn" + item.find('a', class_='product-name').attrs["href"]
            brand = item.find('a', class_='product-brand').text
            price = item.find('div', class_='product-price').findAll('span')[1].text
            if brand != "Minus 417":
                products.append(name)
                links.append(link)
                brands.append(brand)
                prices.append(price)
                count += 1
                print(name)

df = pd.DataFrame(
    {'Product Name': products, 'Brand': brands, 'Price': prices, 'Link': links})
df.to_csv('best_seller_women.csv', index=False, encoding='utf-8')
print('===== DONE =====')
