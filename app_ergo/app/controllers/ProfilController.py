from flask import render_template, session
from app import app
from app.controllers.LoginController import reqlogged
from app.services.servicesGETData import GetDataServices

gds = GetDataServices()

basepath = '/'

@app.route(basepath + 'profil', methods = ['GET'])
@reqlogged
def profil():
    logged = session.get("logged", False)
    username = session.get("username", None)
    data = gds.cards_adopted(session['id'])
    metadata = {"title":"Profil", "pagename": "profil"}
    return render_template('profil.html', metadata=metadata, data=data, logged=logged, username=username)