import os
import time
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# TODO
# 1. Skip the rows that include the ads. 
# 2. Continuously fetch data from all of the pages. 

chrome_options = Options()
chrome_options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")

browser = webdriver.Chrome(f"{os.getcwd()}/chromedriver.exe", options=chrome_options)
link = "https://www.sahibinden.com/alfa-romeo?pagingSize=50"  # Opening the data source page
browser.get(link)
time.sleep(2)
cars = browser.find_elements(by=By.CSS_SELECTOR,
                             value='.searchResultsItem')  # Selecting elements by CSS Class names using "find_elements"

# Making a list of dictionaries to store car data
car_list = []
# Iterating over the web page to fetch individual relevant car information

while True:
    cars = browser.find_elements(by=By.CSS_SELECTOR, value="tr[class*=searchResultsItem]:not([class*=nativeAd])")
    for c in cars:
        time.sleep(random.random())
        model = c.find_elements(by=By.CSS_SELECTOR,
                                value='.searchResultsTagAttributeValue')  # Fetching Series and model as an object
        infos = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsAttributeValue')
        price = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsPriceValue')
        location = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsLocationValue')
        try:  # It will make the code block try and continue executing
            car_list.append(
                {
                    'Model': model[0].text,
                    'Version': model[1].text,
                    'Year': int(infos[0].text),
                    'Km': int(infos[1].text.replace('.', '')),
                    'Color': infos[2].text,
                    'Price': int(price[0].text.replace('.', '').replace('TL', '')),
                    'Location': location[0].text.replace('\n', ' ')
                }
            )
        finally:
            continue
    try:
        next_button = browser.find_element(by=By.CSS_SELECTOR, value='a[class=prevNextBut][title=Sonraki]')
        browser.get(next_button.get_attribute('href'))
        time.sleep((random.random() * 9) + 1)
    except NoSuchElementException:
        break


print(car_list)
time.sleep(3)
browser.close()
