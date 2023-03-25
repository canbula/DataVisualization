import os
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options




# TODO
# 1. Do not get the table rows, which include the advertisement.
# 2. Get the data from the next pages.

firefox_options = Options()
firefox_options.profile = "C:/Users/Keofla/AppData/Roaming/Mozilla/Firefox/Profiles/pj3dzwe2.default"
browser = webdriver.Firefox(options=firefox_options)

link = "https://www.sahibinden.com/alfa-romeo?pagingSize=50"

time.sleep(2)
car_list = []
while True:
    browser.get(link)
    cars = browser.find_elements(by=By.CSS_SELECTOR, value='.searchResultsItem:not(.nativeAd)')
    for c in cars:
        time.sleep(random.random())
        model = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsTagAttributeValue')
        infos = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsAttributeValue')
        price = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsPriceValue')
        location = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsLocationValue')
        try:
            car_list.append(
                {
                'model': model[0].text,
                'version': model[1].text,
                'year': int(infos[0].text),
                'km': int(infos[1].text.replace('.', '')),
                'color': infos[2].text,
                'price': int(price[0].text.replace('.', '').replace('TL', '')),
                'location': location[0].text.replace('\n', ' ')
                }
            )
        finally:
            continue

    try:
        next_page = browser.find_element(by = By.CSS_SELECTOR, value='.prevNextBut[title="Sonraki"]')
        link = next_page.get_attribute("href")
    except:
        break

print(car_list)
time.sleep(5)
browser.close()