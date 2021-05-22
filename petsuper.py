from bs4 import BeautifulSoup
import requests 
import csv
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
 
 
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
 
 
with open('PetSuperMarket.csv', mode="w+", newline='') as f:
  data_writer = csv.writer(f, delimiter=',')
  data_writer.writerow(['Product', 'Price', 'Image Url', ' Description', 'SKU', 'Animal', 'Rating', 'Category'])



d = {"id:" : '"id":', "sku_code:" : '"sku_code":', "url:" : '"url":', "image_url_small" : '"image_url_small"', "image_url_medium" : '"image_url_medium"', "image_url_large" : '"image_url_large"', "name:" : "'name':", "stock:" : "'stock':", "manufacturer:" : '"manufacturer":', "category:" : "'category':", 'category_"id":' : '"category_id":', "sub'category':" : '"subcategory":', "unit_price:" : '"unit_price":', "unit_price_pence:" : '"unit_price_pence":', "description" : '"description"', "currency" : '"currency"',  "shortName" : '"shortName"', "perscriptionRequired" : '"perscriptionRequired"', "lifestage" : '"lifestage"', "species:" : '"species":', "productType" : '"productType"',"hasPromotion" : '"hasPromotion"'}

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text
links = ['Cat/c/PSGB00001', 'Dog/c/PSGB00002']

for link in links:
  for pg in range(0, 47):
    url = f"https://www.pet-supermarket.co.uk/{link}?q=%3Amost-popular&page={pg}"

    req = session.get(url)
    print(req)
    soup = BeautifulSoup(req.content, 'html5lib')

    a = soup.findAll('a', {"class" : "product-item-link"})
    print(len(a))
    href = []


    for i in a:
      an = i.get('href')
      href.append(f"https://www.pet-supermarket.co.uk{an}")

    def save_data(csvfile):
      pet_writer = csv.writer(csvfile, delimiter=',')
      for j in href:
        req = requests.get(j)
        soup = BeautifulSoup(req.content, 'html5lib')

        script = soup.findAll('script')
        data = script[4].text
        o_start = data.find("product:")
        o_end = data.find("user:")
        from ast import literal_eval
        data_ = data[o_start + 8 : o_end - 7]
        y = replace_all(data_,d)
        x = ((y.replace("\n",'' ).replace("			", "").replace("		", '')))
        
        final_data = (json.loads(json.dumps(x)))
        try:
          info = (eval(final_data))
        except:
          continue
        try:
          rate = soup.find("meta", {"itemprop":"ratingValue"})
          rating = rate.get('content')
        except:
          rating = 0
        img = (info['image_url_small'])
        name = (info['name'])
        description = (info['description'])
        sku = (info['sku_code'])
        animal = (info['species'])
        price = (info['unit_price'])
        try:
          cate = soup.find("ol" , {"class" : "breadcrumb"})
          cat = cate.findAll('li')
          
          category = ''
          for c in cat:
            category += f"{c.text} > "
          category = category.replace('\n','')
          category = category[:-2]
        except:
         
          cate = (info['category'])
          if animal == "NoTargetSpecies":
            animal = "Pet"
          category = f"{animal} > {cate}"
        print(name)
        try:
            pet_writer.writerow([name, price, img, description, sku, animal, rating, category ])
            csvfile.flush()
        except:
            pass
        if len(a) == 0:
          break
    with open('PetSuperMarket.csv', mode="a+", newline='') as csvfile:
      save_data(csvfile)
      