import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")

browser = webdriver.Chrome(options=chrome_options)
isThereNextPage = True
pageNumber = 1
link = "https://www.sahibinden.com/alfa-romeo?pagingSize=50"
car_list = []
while isThereNextPage:
    browser.get(link)
    time.sleep(1)
    cars = browser.find_elements(by=By.CSS_SELECTOR, value='.searchResultsItem')
    for c in cars:
        model = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsTagAttributeValue')
        infos = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsAttributeValue')
        price = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsPriceValue')
        location = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsLocationValue')
        #time.sleep(1)
        try:
            car_list.append(
                {
                'model': model[0].text,
                'version': model[1].text,
                'year': int(infos[0].text),
                'km': int(infos[1].text.replace('.', '')),
                'color': infos[2].text,
                'price': {
                    'amount': int(price[0].text.split(" ")[0].replace(".", "")),
                    'currency': price[0].text.split(" ")[1]
                },
                'location': location[0].text.replace('\n', ' ')
                }
            )
        finally:
            continue

    try:
        nextPage = browser.find_element(by=By.CSS_SELECTOR, value='.prevNextBut[title="Sonraki"]')
        pageNumber = pageNumber + 1
        link = nextPage.get_attribute("href")
        isThereNextPage = True
        print(f"Fetching page number: {pageNumber} \t Url: {link}")
        
    except NoSuchElementException:
        isThereNextPage = False

print(len(car_list))
print(car_list)
time.sleep(2)
browser.close()