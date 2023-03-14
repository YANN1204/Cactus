<<<<<<< HEAD
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
    #return render_template('accueil.html', metadata=metadata, data = data)
    return render_template('accueil.html', metadata=metadata)

=======
from flask import render_template, redirect, url_for
from app import app
from app.services.servicesGETData import GetDataServices

ds = GetDataServices()
basepath = '/'

url = "alternative_cards"
urlimp = "impacts"
data = ds.room_by_alternative(url) 


@app.route(basepath, methods = ['GET'])
def accueil():
    data={}
    metadata = {"title": "Accueil", "pagename": "accueil"}
    data["impact"] = int(ds.display_impact(url=urlimp,impacttype="1"))
    data["impact_now"] =ds.display_impact_now()
        
    return render_template('accueil.html', metadata=metadata, data=data,)



>>>>>>> origin/dylan
