from flask import Flask, render_template, url_for
from alfaromeo import AlfaRomeo
import os
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)


@app.route('/')
def index():
    alfa_romeo = AlfaRomeo(
        link="https://canbula.com/alfaromeo/page01.html",
        csv_file=f"{os.getcwd()}/alfaromeo.csv",
        update_interval=3600,
        headless=False
    )
    cars = alfa_romeo.cars()
    average_price = f"{np.round(np.mean([car['price'] for car in cars])):.0f} TL"
    average_km = f"{np.round(np.mean([car['km'] for car in cars])):.0f}"
    average_year = f"{np.round(np.mean([car['year'] for car in cars])):.0f}"
    return render_template(
        'index.html',
        title='Data Visualization Web Application',
        cars=cars,
        average_price=average_price,
        average_km=average_km,
        average_year=average_year,
        km_vs_price=km_vs_price(cars),
        model_histogram=model_histogram(cars),
        city_pie=city_pie(cars)
    )

def km_vs_price(cars):
    km = []
    price = []
    for car in cars:
        km.append(car['km'])
        price.append(car['price'])
    fig = plt.figure()
    plt.scatter(km, price)
    plt.xlabel("KM")
    plt.ylabel("Price [TL]")
    plt.title("KM vs Price")
    plt.xticks(rotation=0,
               ticks=range(0, 600000, 100000),
               labels=[f"{x//1000}K" for x in range(0, 600000, 100000)])
    plt.semilogy()
    plt.yticks(rotation=0,
               ticks=[100000, 200000, 500000, 1e6, 2e6, 5e6],
               labels=["100K", "200K", "500K", "1M", "2M", "5M"])
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')

def model_histogram(cars):
    model = []
    for car in cars:
        model.append(car['model'])
    fig = plt.figure(figsize=(12, 5))
    plt.subplots_adjust(bottom=0.35)
    plt.hist(model, bins=range(0, len(set(model))+1), align='left', rwidth=0.8)
    plt.xlabel('Model')
    plt.ylabel('Count')
    plt.title('Model Histogram')
    plt.xticks(rotation=90)
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')

def city_pie(cars):
    city = []
    for car in cars:
        city.append(car['location'].split(' ')[0])
    city_counts = {}
    for c in city:
        if c in city_counts:
            city_counts[c] += 1
        else:
            city_counts[c] = 1
    top_5 = sorted(city_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    top_5_cities = [x[0] for x in top_5]
    other = 0
    for c in city_counts:
        if c not in top_5_cities:
            other += city_counts[c]
    fig = plt.figure(figsize=(12, 5))
    plt.pie([x[1] for x in top_5] + [other],
            labels=[x[0] for x in top_5] + ['Other'],
            autopct='%1.1f%%')
    plt.title('City Pie Chart')
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')


if __name__ == '__main__':
    app.run()
