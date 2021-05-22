import requests
from bs4 import BeautifulSoup
import csv
import subprocess
import sys
try:
  from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
  from selenium import webdriver
  from selenium.webdriver.support.ui import WebDriverWait
  from selenium.webdriver.support import expected_conditions as EC
  from selenium.webdriver.common.by import By
except:
  subprocess.check_call([sys.executable, "-m", "pip", "install", 'selenium'])
  from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
  from selenium import webdriver
  from selenium.webdriver.support.ui import WebDriverWait
  from selenium.webdriver.support import expected_conditions as EC
  from selenium.webdriver.common.by import By

from time import sleep
import json
import csv
from time import sleep
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext





session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
 
chrome_options = webdriver.ChromeOptions()
# chrome_options.page_load_strategy = 'none'
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
chrome_options.add_argument("start-maximized") 
 
chrome_options.add_argument("--no-sandbox") 
chrome_options.add_argument("--disable-infobars") 
chrome_options.add_argument("--disable-dev-shm-usage") 
chrome_options.add_argument("--disable-browser-side-navigation") 
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
prefs = {"profile.default_content_setting_values.notifications" : 2}
prefs = {"credentials_enable_service", False}
prefs = {"profile.password_manager_enabled" : False}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)


with open('Fetch.csv', mode="w+", newline='') as f:
  data_writer = csv.writer(f, delimiter=',')
  data_writer.writerow(['Product', 'Price', 'Image Url', ' Description', 'SKU', 'Animal', 'Rating', 'Category'])

links = ['small-pets', 'cats',  'birds-wildlife', 'healthcare', 'dogs']

for l in links:
  def save_data(csvfile):
    pet_writer = csv.writer(csvfile, delimiter=',')
    url = f"https://fetch.co.uk/{l}"
    # url = 'https://fetch.co.uk/dogs/dog-pet-tech'
    SCROLL_PAUSE_TIME = 6
    TIMEE = 0
    driver.get(url)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        TIMEE += SCROLL_PAUSE_TIME
        try:
          WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='__next']/div/div[2]/div[1]/div[2]/div/div/div[2]/div[5]/div[2]/button"))).click()
          print(f"Clicked on Button at {TIMEE} Second")
        except:
          print(f"Scrolling Website => {TIMEE}")
        if new_height == last_height:
        # if TIMEE == 6:
            break
        last_height = new_height

    req = driver.page_source
    sleep(1)
    soup = BeautifulSoup(req, 'html5lib')

    a = soup.findAll('a', {"class" : "ProductTitleWithMeasureLink__AnchorComponent-sc-9il80e-1 cJMQDX"})
    rate = soup.findAll('span', {"class" : "bv-off-screen"})
    href = []
    for link in a:
      an = link.get('href')
      href.append(f"https://fetch.co.uk{an}")

    print(len(href))
    t_i = 0
    for idx,j in enumerate(href):
      req = session.get(j)
      soup = BeautifulSoup(req.content, 'html5lib')
      
      try:
        script = soup.find('script', {"id" : "__NEXT_DATA__"}).text
      except:
        print("Paseed")
        continue
      try:
        rating = rate[idx].text.rsplit(' ')[0]
      except:
        rating = 0
      data = json.loads(script)
      # print(d['props'].keys())
      info = (data['props']['pageProps'])
      # print(info)
      sku = (info['sku'])
      name = (info['productGroup']['name'])
      img = (info['productGroup']['images'])
      des = (info['productGroup']['content'])
      
      try:
          try:
            if (info['productGroup']['priceRange']['from']['amount']):
              continue
            price = (info['productGroup']['unitPrice']['price']['amount'])
            
          except KeyError:
            price = (info['productGroup']['prices']['base']['amount'])
      except:
        continue
    
        # price = (info['productGroup']['priceRange']['from']['amount'])

      # rate = soup.find("div", {"class" : "bv-secondary-rating-summary-list bv-table"})
      
      animal = info['productGroup']['fullCategories'][1]['name']
      cate1 = info['productGroup']['fullCategories'][2]['name']
        
      try:
        cate2 = info['productGroup']['fullCategories'][3]['name']
        category = f"{cate1} > {cate2}"
      except:
        category = cate1

      if animal == 'HealthCare' or animal == 'Special Offers':
        animal = 'Not Categorized'
      print(f"{idx}- {name}")
      

      # rating = soup.find("span", {"itemprop": "ratingValue"})
      description = ""
      for d in des:
        description += (d['content'])
      try:
        description = cleanhtml(description)
      except:
        pass
      for i in img:
        image1 = (i['url'])

      image = f"https:{image1}"
      
      try:
          pet_writer.writerow([name, price, image, description, sku, animal, rating, category ])
          csvfile.flush()
      except:
          pass


  with open('Fetch.csv', mode="a+", newline='') as csvfile:
      save_data(csvfile)
       