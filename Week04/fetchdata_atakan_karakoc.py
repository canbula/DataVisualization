import os
import time
import random
import csv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
browser = webdriver.Chrome(f"{os.getcwd()}/chromedriver", options=chrome_options)
link = "https://www.sahibinden.com/alfa-romeo?pagingSize=50"
car_list = []
isNextPage = True

#A loop for the next pages
while isNextPage:
    browser.get(link)
    time.sleep(2)
    cars = browser.find_elements(by=By.CSS_SELECTOR, value='.searchResultsItem')
    for c in cars:
        #To skip advertisement lines
        if c.get_attribute('data-id') is None:
            continue
        else:
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
    #Getting the link to the next page
    try:
        isNextPage = browser.find_element(By.CSS_SELECTOR, value='.prevNextBut[title="Sonraki"]')
        link = isNextPage.get_attribute("href")
        isNextPage = True
    except NoSuchElementException:
        isNextPage = False

print(car_list)
time.sleep(5)
browser.close()
print(len(car_list))

# with open('cars.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(['model', 'version', 'year', 'km', 'color', 'price', 'location'])
#     for car in car_list:
#         writer.writerow([car['model'], car['version'], car['year'], car['km'], car['color'], car['price'], car['location']])