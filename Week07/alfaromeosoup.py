import requests
import re
from bs4 import BeautifulSoup
import time
import random
import csv
import os


class AlfaRomeo:
    def __init__(self, domain, link, csv_file, update_interval):
        self.domain = domain
        self.link = link
        self.csv_file = csv_file
        self.update_interval = update_interval
        self.__car_list = []

    def update_cars(self):
        car_list = []
        url = f"{self.domain}{self.link}"
        # url = "https://www.sahibinden.com/alfa-romeo?pagingSize=50"
        # url = "https://www.canbula.com/alfaromeo/page01.html"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }
        next_page = True
        while next_page:
            result = requests.get(url, headers=headers)
            result = re.sub(r"<br\s*/?>", '\n', result.text)
            soup = BeautifulSoup(result, "html.parser", from_encoding="utf-8")
            rows = soup.find_all("tr", {"class": "searchResultsItem", "data-id": True})
            for row in rows:
                model = row.find_all("td", {"class": "searchResultsTagAttributeValue"})[0].text.strip()
                version = row.find_all("td", {"class": "searchResultsTagAttributeValue"})[1].text.strip()
                year = int(row.find_all("td", {"class": "searchResultsAttributeValue"})[0].text.strip())
                km = int(row.find_all("td", {"class": "searchResultsAttributeValue"})[1].text.strip().replace(".", ""))
                color = row.find_all("td", {"class": "searchResultsAttributeValue"})[2].text.strip()
                price = int(row.find("td", {"class": "searchResultsPriceValue"}).text.strip().split(",")[0].replace(".", "").replace("TL", ""))
                location = row.find("td", {"class": "searchResultsLocationValue"}).text.strip().replace("\n", " ")
                car_list.append(
                    {
                        "model": model,
                        "version": version,
                        "year": year,
                        "km": km,
                        "color": color,
                        "price": price,
                        "location": location
                    }
                )
            next_link = soup.find("a", {"class": "prevNextBut", "title": "Sonraki"})
            if next_link is None:
                next_page = False
            else:
                next_page = True
                url = f"{self.domain}{next_link.get('href')}"
            time.sleep(random.randint(1, 5)+random.random())
        self.__car_list = car_list
    
    def save_cars(self):
        with open(self.csv_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["model", "version", "year", "km", "color", "price", "location"])
            writer.writeheader()
            for car in self.__car_list:
                writer.writerow(car)
    
    def load_cars(self):
        with open(self.csv_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            self.__car_list = [row for row in reader]
    
    def delete_cars(self):
        self.__car_list = []
        try:
            os.remove(self.csv_file)
        except:
            pass
    
    def cars(self):
        if not os.path.exists(self.csv_file) or (time.time() - os.path.getmtime(self.csv_file)) > self.update_interval:
            self.update_cars()
            self.save_cars()
        else:
            self.load_cars()
        return self.__car_list


if __name__ == "__main__":
    alfa_romeo = AlfaRomeo(
        "https://www.sahibinden.com", 
        "/alfa-romeo?pagingSize=50", 
        f"{os.getcwd()}/Week07/alfa_romeo.csv", 
        36000
    )
    cars = alfa_romeo.cars()
    print(cars)
