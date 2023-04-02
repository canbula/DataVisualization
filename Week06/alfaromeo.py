import os
import time
import random
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager
from selenium.webdriver.common.by import By


class AlfaRomeo:
    def __init__(self, link, csv_file="./alfaromeo.csv", update_interval=1200, headless=True):
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        self.link = link
        self.csv_file = csv_file
        self.update_interval = update_interval
        self.__car_list = []

    def update_cars(self):
        car_list = []
        next_page = True
        link = self.link
        while next_page:
            self.browser.get(link)
            time.sleep(1 + random.random())
            cars = self.browser.find_elements(by=By.CSS_SELECTOR, value=".searchResultsItem")
            for c in cars:
                if c.get_attribute("data-id") is None:
                    continue
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
                except:
                    continue
            time.sleep(1 + random.random())
            next_link = self.browser.find_elements(by=By.CSS_SELECTOR, value=".prevNextBut")
            next_page = False if len(next_link) == 0 else True
            for n in next_link:
                if n.get_attribute("title") == "Sonraki":
                    link = n.get_attribute("href")
                    next_page = True
                else:
                    next_page = False
        self.browser.close()
        return car_list

    def save_cars(self):
        with open(self.csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            for c in self.__car_list:
                writer.writerow([
                    c['model'], c['version'], c['year'], c['km'], c['color'], c['price'], c['location']
                ])

    def load_cars(self):
        with open(self.csv_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    self.__car_list.append({
                        'model': row[0],
                        'version': row[1],
                        'year': int(row[2]),
                        'km': int(row[3]),
                        'color': row[4],
                        'price': int(row[5]),
                        'location': row[6]
                    })
                except:
                    continue

    def delete_cars(self):
        try:
            os.remove(self.csv_file)
        except:
            pass

    def cars(self):
        if not os.path.exists(self.csv_file) or (time.time() - os.path.getmtime(self.csv_file)) > self.update_interval:
            self.__car_list = self.update_cars()
            self.save_cars()
        else:
            self.load_cars()
        return self.__car_list


if __name__ == "__main__":
    alfa_romeo = AlfaRomeo(
        link="https://canbula.com/alfaromeo/page01.html",
        csv_file=f"{os.getcwd()}/alfaromeo.csv",
        update_interval=3600,
        headless=False
    )
    cars = alfa_romeo.cars()
    print(cars)
