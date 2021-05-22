import requests
from bs4 import BeautifulSoup
import csv
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


links = ['d34/cat_food', 'd7/dog_food', 'd2/dog_products', 'd418/cat_litter', 'other_small_furries']
animal_ = ['Cat', 'Dog', 'Dog', 'Cat', 'Small Furries']

with open('petplanet_data.csv', mode="w+", newline='') as f:
  data_writer = csv.writer(f, delimiter=',')
  data_writer.writerow(['Product', 'Price', 'Image Url', ' Description', 'SKU', 'Animal', 'Rating', 'Category'])

for z in range(len(links)):
  url = f"https://www.petplanet.co.uk/{links[z]}?page_size=3600"
  animal = animal_[z]  
  req = requests.get(url)

  soup = BeautifulSoup(req.content, 'html5lib')

  anchors = soup.findAll('a', {"class" : "thumbLink"})
  print(len(anchors))

  href = []



  for i in anchors:
    a = i.get('href')
    href.append(f"https://www.petplanet.co.uk/{a}")
    # print(a)
  def save_data(csvfile):
    pet_writer = csv.writer(csvfile, delimiter=",")
    for j in range(len(href)):
      req = session.get(href[j])
      soup = BeautifulSoup(req.content, 'html5lib')
      try:
        img_div = soup.find('div', {"class" : "img-holder"})
        img = img_div.find('img')
        image = f"https://www.petplanet.co.uk{img['src']}"
      except:
        continue
      div = soup.find('div', {"class" : 'title'})
      name = div.find('h1')
      try:
        price = soup.find('span', {"class" : "price"})
        price_ = price.text 
      except:
        price = soup.find('p', {"class" : "price"}) 
        price_ = price.text 
      description = soup.find('div', {"class" : "description"}) 
      cate = soup.find('div', {"class" : "crumbs"}).text
      c = cate.replace("\n", "")
      ca = c.replace("  ", "")
      
      category = ca.rsplit('›', 1)[0] 
      print(f"{j}- {name.text}")
      
      json_data = soup.findAll('script', {"type" : "application/ld+json"})
      
      
      data = json_data[1].text
      
      o_start = data.find("ratingValue")
      o_end = data.find("reviewCount")
      rating = data[o_start + 16: o_end - 9 ]
      try: 
        pet_writer.writerow([name.text, price_, image, description.text, '', animal, rating, category])  
        csvfile.flush()
      except:
          pass
  with open('petplanet_data.csv', mode="a+", newline='') as csvfile:
    save_data(csvfile)
