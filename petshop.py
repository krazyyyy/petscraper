import requests
from bs4 import BeautifulSoup
import csv
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


with open('Petshop_data.csv', mode="w+", newline='') as f:
  data_writer = csv.writer(f, delimiter=',')
  data_writer.writerow(['Product', 'Price', 'Image Url', ' Description', 'SKU', 'Animal', 'Rating', 'Category'])
 
pages = ['Other-Pets/Bird','Other-Pets/Horse', 'Dog' , 'Cat'  ]
def save_data(csvfile):
  pet_writer = csv.writer(csvfile, delimiter=',')
  """
  Change This Url To Scrape Other Categories For Example
  To Scrape Cat Change it to
  url_ = 'https://www.petshop.co.uk/cat'
  For Bird
  url_ = 'https://www.petshop.co.uk/Other-Pets/Bird'

  as well change the Name Of Animal According to it
  """
  # Change This URL To Extract Other Data
  url_ = 'https://www.petshop.co.uk/Cat'
  # Change This Name According To Animal
  animal_ = "Cat"
  req_ = requests.get(url_)
  
  soup = BeautifulSoup(req_.content, 'html5lib')

  cate = soup.findAll('a', {"class" : "facets-category-cell-anchor"})
    

  href = []
   
  href_ = []
  category = []
  for y in cate:
    a = y.get('href')
    href_.append(f"https://www.petshop.co.uk{a}")
  for web in href_:
    for z in range(1, 9):
      if z == 1:
        url = web
      else:
        url = f"{web}?page={z}"
      print(url)
      reqs = requests.get(url)
      soups = BeautifulSoup(reqs.content, 'html5lib')
      
      
      
     
      anchors = soups.findAll('a', {'class' :'facets-item-cell-grid-title'})
      print(len(anchors))
      for i in anchors:
        cat = soups.find('title').text
        a = i.get('href')
        category.append(cat)
        href.append(f"https://www.petshop.co.uk{a}")
      
      print(len(category))
  for j in range(len(href)):
   
    req = session.get(href[j])
    soup = BeautifulSoup(req.content, 'html5lib')

    name = soup.find('h1', {'itemprop' : 'name'})
    try:
      description_ = soup.find('div', { 'class' : 'product-details-information-tab-content-container'})
      description = description_.text
    except:
      description = '' 
    sku = soup.find('span', {'itemprop' : 'sku'})
    price = soup.find('meta', {'itemprop' : "price"})
    rating = soup.find('meta', {'itemprop' : 'ratingValue'})
    
    if name == None:
      continue

    print(f"{j}-{name.text}")
    try:
      img = soup.find('img', {'itemprop' : 'image'})
      image = img['src']
    except:
      li = soup.find('li', {"class" : 'product-details-image-gallery-container' })
      img = li.find('img')
      image = img['src']
    try:
        pet_writer.writerow([name.text, price.get('content'), image, description, sku.text, animal_, rating.get('content'), category[j] ])
        csvfile.flush()
    except:
        pass
# z += 1  
with open('Petshop_data.csv', mode="a+", newline='') as csvfile:
  save_data(csvfile)