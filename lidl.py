import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.lidl.co.uk/en/c/orlando-dog-dental-chews/c100'

with open('LIDL.csv', mode="w+", newline='') as f:
  data_writer = csv.writer(f, delimiter=',')
  data_writer.writerow(['Product', 'Price', 'Image Url', ' Description', 'SKU', 'Animal', 'Rating', 'Category'])

req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

anchor = soup.findAll('a', {"class" : "product__body"})
print(len(anchor))
href = []
for i in anchor:
  a = i.get('href')
  href.append(f"https://www.lidl.co.uk{a}")
def save_data(csvfile):
  pet_writer = csv.writer(csvfile, delimiter=',')
  for j in range(len(href)):
    req = requests.get(href[j])
    soup = BeautifulSoup(req.content, 'html5lib')

    price = soup.find('div', {"class" : "pricebox__price-wrapper"})
    n = soup.find('h1', {'itemprop' : "name"}).text
    category = soup.find('div', {'class' : 'breadcrumbs__text'})
    description = soup.find('article', {"class" : "textbody"})
    img = soup.find('div', {"class" : "multimediabox__preview"})
    image = img.find('img')
    # print(name.text)
    name = n.replace("   ", "")
    name = n.replace("\n", "")
    print(f"{j}- {name}")
    if 'Cat' in name:
      animal = 'Cat'
    elif 'Dog' in name:
      animal = 'Dog'
    else:
      animal = 'Not Categorized'
    try:
      pet_writer.writerow([name, price.get('aria-label'), image['src'], description.text, '', animal, '', category.text])
    except:
      pass
with open('LIDL.csv', mode="a+", newline='') as csvfile:
  save_data(csvfile)