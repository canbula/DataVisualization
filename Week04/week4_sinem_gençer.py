import os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import random
from selenium.common.exceptions import NoSuchElementException

humanface = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
link = "https://www.sahibinden.com/alfa-romeo?pagingSize=50"
path = "E:\6. Dönem\Data Vis\Codes\chromedriver.exe"

chrome_options = Options()
chrome_options.add_argument("user-agent={0}".format(humanface))
#chrome_options.add_argument("--headless")

browser = webdriver.Chrome(path, options=chrome_options)
browser.get(link)
time.sleep(2)
car_list=[]

existsNextPage = True

while existsNextPage:
    cars = browser.find_elements(by=By.CSS_SELECTOR, value='.searchResultsItem:not(.nativeAd)')
    for c in cars:
        model = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsTagAttributeValue')
        infos = c.find_elements(by=By.CSS_SELECTOR, value ='.searchResultsAttributeValue')
        price = c.find_elements(by=By.CSS_SELECTOR, value ='.searchResultsPriceValue')
        location = c.find_elements(by=By.CSS_SELECTOR, value ='.searchResultsLocationValue')
        try:
            car_list.append(
            {
            'model':model[0].text,
            'version':model[1].text,
            'year':int(infos[0].text),
            'km':int(infos[1].text.replace('.', '')),
            'color':infos[2].text,
            'price':int(price[0].text.replace('.','').replace('TL','')),
            'location':location[0].text.replace('\n',' ')
            }
        )
        finally:
            continue
    try:
        next_button= browser.find_element(by=By.CSS_SELECTOR, value='.prevNextBut[title="Sonraki"]')
        next_button.click()
    except NoSuchElementException:
        existsNextPage = False

print(car_list)
time.sleep(5)
browser.close()