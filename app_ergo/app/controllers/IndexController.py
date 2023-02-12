from flask import render_template, redirect, url_for
from app import app
from app.services.servicesData import DataServices

ds = DataServices()
basepath = '/'

url = "fiche"
data = ds.room_by_alternative(url)

@app.route(basepath, methods = ['GET'])
def index():
    return render_template('index.html', data = data)

