import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
browser = webdriver.Chrome(f"{os.getcwd()}/chromedriver", options=chrome_options)
link = "https://www.sahibinden.com/alfa-romeo?pagingSize=50"
browser.get(link)
time.sleep(2)
car_list = []
while True:
    cars = browser.find_elements(by=By.CSS_SELECTOR, value='tr[class*=searchResultsItem]:not([class*=nativeAd])')
    for c in cars:
        try:
            model = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsTagAttributeValue')
            infos = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsAttributeValue')
            price = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsPriceValue')
            location = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsLocationValue')
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
        next_button = browser.find_element(by=By.CSS_SELECTOR, value='a[class=prevNextBut][title=Sonraki]')
        browser.get(next_button.get_attribute('href'))
        time.sleep(random.random() + 1)
    except NoSuchElementException:
        break

print(car_list)
time.sleep(5)
browser.close()
