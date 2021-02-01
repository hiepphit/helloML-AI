

#Using Requests Library
import requests
from bs4 import BeautifulSoup
import pandas as pd

brandNames = []  # List to store brand of the product
links = []  # List to store detail link of the product
histories = []  # List to store detail link of the product

count = 0
response = requests.get("https://www.notino.fr/parfums-homme/")
soup = BeautifulSoup(response.content, "html.parser")

body = soup.findAll('li', attrs={'class': 'item-filtered'})
print(body)
# options = body[0].findAll('li')

# for i in options:
#     name = i.find('a').find('span').text
#     print(name)


# for a in options[:-1]:
#     brandNames.append(a.text)
#     link = "https://www.thegioinuochoa.com.vn/"+a.attrs["value"]+"/"
#     links.append(link)
#     resBrand = requests.get(link)
#     rs = BeautifulSoup(resBrand.content, "html.parser")
#     history = rs.find('div', class_='brands-history')
#     if history:
#         histories.append(history.text[1:])
#     else:
#         histories.append('null')
#     count+=1
#     print(count)

# df = pd.DataFrame(
#     {'Brand Name': brandNames, 'Link': links, 'History': histories})
# df.to_csv('list_brand.csv', index=False, encoding='utf-8')
# print('===== DONE =====')
