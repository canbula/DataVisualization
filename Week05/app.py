from flask import Flask
from flask import render_template
from alfaromeo import AlfaRomeo
import os


app = Flask(__name__)


@app.route('/')
def index():
    alfa_romeo = AlfaRomeo(
        link="https://canbula.com/alfaromeo/page01.html",
        csv_file=f"{os.getcwd()}/Week05b/alfaromeo.csv",
        update_interval=3600,
        headless=False
    )
    return render_template("index.html", 
                           cars=alfa_romeo.cars(), 
                           title="Alfa Romeo Cars"
                           )


if __name__ == "__main__":
    app.run(debug=True)
