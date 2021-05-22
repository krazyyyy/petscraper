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




url = [
      'https://www.aldi.co.uk/c/specialbuys/pets/dog-and-puppy-supplies',
      'https://www.aldi.co.uk/c/specialbuys/pets/rabbits-birds-and-small-animal-accessories',
      'https://www.aldi.co.uk/c/specialbuys/pets/cats-and-kitten-supplies',
      'https://www.aldi.co.uk/c/specialbuys/gifts/gifts-for-pets']

animal_ = ['Dog', 'Small Animal', 'Cats', 'Not Categorized']
with open('ALDI.csv', mode="w+",newline='') as f:
  pet_writer = csv.writer(f, delimiter=",")
  pet_writer.writerow(['Product', 'Price', 'Image Url', ' Description', 'SKU', 'Animal', 'Rating', 'Category'])

def save_data(csvfile):
  pet_writer = csv.writer(csvfile, delimiter=',')
  for index in range(len(url)): 
    driver.get(url[index])
    sleep(10)
    animal = animal_[index]
    href = []
    for i in range(2, 30):
      try:
        sleep(3)
        # driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f"/html/body/main/div[2]/div[4]/div[3]/div[2]/div/div[6]/div[{i}]/a[1]"))))
        d = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f"/html/body/main/div[2]/div[4]/div[3]/div[2]/div/div[6]/div[{i}]/a[1]")))
        href.append(d.get_attribute('href'))
      except:
        pass
    print(len(href))
    for j in range(len(href)):
      
      req = requests.get(href[j])
      soup = BeautifulSoup(req.content, 'html5lib')
      datas =  soup.find('script', {"type" : "application/ld+json"}).text
      # print(data)
      data = json.loads(datas)
      category = 'Home > Pets'
      rating = data['aggregateRating']['ratingValue']
      desctiption = data['description']
      name = data['name']
      sku = data['sku']
      price = data['offers']['price']
      image = data['image']
      print(f"{j}- {name}")

      pet_writer.writerow([name, price, image, desctiption, sku, animal, rating, category])
      csvfile.flush()
      
with open('ALDI.csv', mode="a+", newline='') as csvfile:
  save_data(csvfile)  