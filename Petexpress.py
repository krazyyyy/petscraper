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



with open('petexpress.csv', mode="w+", newline='') as f:
  data_writer = csv.writer(f, delimiter=',')
  data_writer.writerow(['Product', 'Price', 'Image Url', ' Description', 'SKU', 'Animal', 'Rating', 'Category'])

links = ['birds-aviary-supplies', 'fish-aquatic-supplies', 'birds-aviary-supplies', 'dog-puppy-supplies', 'cats-kitten-supplies', 'rabbit-small-animals']
animals = ['Birds', 'Fish', 'Reptiles', 'Dog', 'Cat', 'Small Pets']

for y in range(len(links)):
  url = f"https://www.thepetexpress.co.uk/{links[y]}/"

  req = requests.get(url)
  print(req)
  soup = BeautifulSoup(req.content, 'html5lib')

  div = soup.find('div', {"class" : "pg-case-inner"})
  a = div.findAll('a')
  print(len(a))

  href = []


  def save_data(csvfile):
    pet_writer = csv.writer(csvfile, delimiter=",")
    for i in a[1:]:
      a_ = i.get('href')
      if a_[0] != "/":
        a_ = f"/{a_}"
      href.append(f"https://www.thepetexpress.co.uk{a_}")


    for j in href:
      for z in range(1, 5):
        print(j)
        req = requests.get(f"{j}?limit=480&pg={z}")
        soup = BeautifulSoup(req.content, 'html5lib')

        div = soup.findAll('div', {"class" : "category-page"})
        print(len(div))
        
        anchors = []

        #if Another Sub Category Exists
        if len(div) == 0:
          soup2 = BeautifulSoup(req.content, 'html5lib')

          div2 = soup2.find('div', {"class" : "pg-case-inner"})
          a2 = div2.findAll('a')
          print(len(a2))

          subs = []

          for t in a2[1:]:
            a_2 = t.get('href')
            subs.append(f"https://www.thepetexpress.co.uk{a_2}")
          for s in subs[1:]:
            print(s)
            req3 = session.get(f"{s}")
            soup3 = BeautifulSoup(req3.content, 'html5lib')

            div_ = soup3.findAll('div', {"class" : "category-page"})
            print(len(div_))
        #     #Checking For Third Sub category
            if len(div_) == 0: 
              # soup4 = BeautifulSoup(req.content, 'html5lib')

              div4 = soup3.find('div', {"class" : "pg-case-inner"})
              a4 = div4.findAll('a')
              print(len(a4))
              subscat = []
              for g in a4[1:]:
                
                a_4 = g.get('href')
                subscat.append(f"https://www.thepetexpress.co.uk{a_4}")
              divtwo = []
              for su in subscat[1:]:
                req4 = session.get(su)
                soup4 = BeautifulSoup(req4.content, 'html5lib')

                div_2 = soup4.findAll('div', {"class" : "category-page"})
                divtwo.extend(div_2)
                print(len(divtwo))

        if "divtwo" not in locals():
          divtwo = []

        if "div_" not in locals():
            div_ = []
          #till here
        for d2 in divtwo:
          an = (d2.find('a'))
          anchors.append(f"https://www.thepetexpress.co.uk{an.get('href')}")

        for d_ in div_:
          an = (d_.find('a'))
          anchors.append(f"https://www.thepetexpress.co.uk{an.get('href')}")

        for d in div:
          an = (d.find('a'))
          anchors.append(f"https://www.thepetexpress.co.uk{an.get('href')}")
        
        for idx,link in enumerate(anchors):
          req = session.get(link)
          soup = BeautifulSoup(req.content, 'html5lib')

          data_ = soup.find('script', {"type" : "application/ld+json"}).text
          animal = animals[y]
          data = json.loads(data_)
          try:
              cate = soup.find('ol', {"class" : "breadcrumb"})
              cate_ = cate.findAll('li')
              cat = ''
              for c in cate_:
                cat += f"{c.text} >"
              
              cate_ = cat.replace('Home >', '')
              category = cate_[:-1]
          except:
            cate = soup.find('ol', {"class" : "breadcrumb"})
            cate_ = cate.text.replace('&', '>')
            cate_ = cate.text.replace(' ', ' > ')
            category = cate_.rsplit('>', 1)[0]
          try:
            rating = data['aggregateRating']['ratingValue']
          except:
            rating = 0
          try:
            price = data['offers']['price']
          except:
            price_ = (data['offers'])
            for p in price_[1:2]:
              price = p['price']
          description = data['description']
          SKU = data['sku'][0]
          name = data['name']
          image = data['image'][0]
          print(f"{idx}- {name}")
          try: 
            pet_writer.writerow([name, price, image, description, SKU, animal, rating, category])  
            csvfile.flush()
          except:
              pass

        if len(div) != 480:
          print("Breaked")
          break

  with open('petexpress.csv', mode="a+", newline='') as csvfile:
    save_data(csvfile)
       
