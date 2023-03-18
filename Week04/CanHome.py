import os
import time
import random

import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio

class Car:

    def __init__(self,model,version,year,km,color,price,location):
        self.model=model
        self.version=version
        self.year=year
        self.km=km
        self.color=color
        self.price=price
        self.location=location


    def __str__(self):

        return f"model: {self.model} year: {self.year} version:{self.version} km:{self.km} color:{self.color} price:{self.price} location:{self.location}"

# decorator for exception handler
def exception(func):



    def excpt(*args,**kwargs):
        cardec_list=[]
        try:
            cardec_list=func(*args, **kwargs)
        except NoSuchElementException:
            print(" process  finished")

        finally:

            return cardec_list
    return excpt


# TODO
# 1. Do not get the table rows, which include the advertisement.
# 2. Get the data from the next pages.


chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                            " Chrome/111.0.0.0 Safari/537.36'"
)

browser = webdriver.Chrome(f"{os.getcwd()}/chromedriver", options=chrome_options)

link = "https://www.sahibinden.com/alfa-romeo?pagingSize=50"
browser.maximize_window()

browser.get(link)
time.sleep(5)




@exception
def fetchDataaFromOnePage(car,cars_array):

    car_list = []
    for i,c  in enumerate(car):

        classOfElement=c.get_attribute("class").split(' ')

        if 'nativeAd'  not in classOfElement:


            time.sleep(random.random())
            model = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsTagAttributeValue')

            infos = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsAttributeValue')
            price = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsPriceValue')
            location = c.find_elements(by=By.CSS_SELECTOR, value='.searchResultsLocationValue')


            modelcar = model[0].text,
            versioncar =model[1].text,
            yearcar = int(infos[0].text.lstrip()),
            kmcar = int(infos[1].text.replace('.', '')),
            colorcar = infos[2].text,
            pricecar = int(price[0].text.replace('.', '').replace('TL', '')),
            locationcar = location[0].text.replace('\n', ' ')

            car=Car(modelcar, versioncar, yearcar, kmcar, colorcar, pricecar, locationcar)
            print(str(car))

            cars_array.append(car)
            car_list.append(car)

        '''
        car_list.append(
                {
                'model': model[0].text,
                'version': model[1].text,
                'year': int(float(infos[0].text.lstrip())),
                'km': int(infos[1].text.replace('.', '')),
                'color': infos[2].text,
                'price': int(price[0].text.replace('.', '').replace('TL', '')),
                'location': location[0].text.replace('\n', ' ')
                }
                )
        '''
    return car_list


@exception
def fetchDataAllOfThem(cars_array):
    page_num=1
    i=1
    while True:
        print(f"******************************PAGE NUMBER: {page_num}************************************************")
        time.sleep(5)
        cars = browser.find_elements(by=By.CSS_SELECTOR, value='.searchResultsItem')
        fetchDataaFromOnePage(cars,cars_array)

        xpath = f"//*[@id='searchResultsSearchForm']/div/div[4]/div[3]/div[1]/ul/li[1{i}]"
        prev_next_button=browser.find_element_by_xpath(xpath).find_element_by_css_selector("a")

        browser.execute_script("arguments[0].click();",prev_next_button)
        page_num+=1

        if i==1 or page_num==6:
            i+=1

carss=[]
fetchDataAllOfThem(carss)

print(f"araba sayısı:{len(carss)} ")
time.sleep(5)
browser.close()