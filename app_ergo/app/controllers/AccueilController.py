from flask import render_template, redirect, url_for
from app import app
from app.services.servicesGETData import GetDataServices
from app.models.dataDAO import DataDAO

ds = GetDataServices()
basepath = '/'

list_item = ['alternative_cards', 'alternative_cards_tags', 'comments', 'forums', 'forums_tags', 'impacts',
             'rooms', 'tags', 'users', 'users_alternative_cards', 'users_tags']

url = "alternative_cards"
urlimp = "impacts"
data = ds.room_by_alternative(url) 


@app.route(basepath, methods = ['GET'])
def accueil():
    data={}
    metadata = {"title": "Accueil", "pagename": "accueil"}
    data["impact"] = int(ds.display_impact(url=urlimp,impacttype="1"))
    data["impact_now"] = ds.display_impact_now()
        
    return render_template('accueil.html', metadata=metadata, data=data,)



