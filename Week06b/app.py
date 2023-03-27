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
        update_interval=136000,
        headless=False
    )
    cars = alfa_romeo.cars()
    return render_template(
        'index.html',
        title="Data Visualization Web Application",
        cars=cars,
        km_vs_price=km_vs_price(cars)
    )

def km_vs_price(cars):
    km = []
    price = []
    for car in cars:
        km.append(car['km'])
        price.append(car['price'])
    fig = plt.figure()
    plt.scatter(km, price)
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')


if __name__ == '__main__':
    app.run()
