from flask import render_template, session, url_for

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
    data = {}
    data['cards_adopted'] = gds.cards_adopted(session['userId'])
    data['cards_suggested'] = gds.cards_suggested(session['userId'])
    data['impact'] = []
    metadata = {"title":"Profil", "pagename": "profil"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}
    return render_template('profil.html', metadata=metadata, data=data, logged=logged, username=username, images=images)