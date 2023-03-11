from flask import render_template, redirect, url_for
from app import app
from app.services.servicesGETData import GetDataServices

ds = GetDataServices()
basepath = '/'

url = "alternative_cards"
data = ds.room_by_alternative(url) 


@app.route(basepath, methods = ['GET'])
def accueil():
    metadata = {"title": "Accueil", "pagename": "accueil"}
    return render_template('accueil.html', metadata=metadata, data = data)

