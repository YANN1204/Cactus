from flask import render_template, session
from app import app
from app.controllers.LoginController import reqlogged

basepath = '/'

@app.route(basepath + 'profil', methods = ['GET'])
@reqlogged
def profil():
    logged = session.get("logged", False)
    username = session.get("username", None)
    metadata = {"title":"Profil", "pagename": "profil"}
    return render_template('profil.html', metadata=metadata, logged=logged, username=username)