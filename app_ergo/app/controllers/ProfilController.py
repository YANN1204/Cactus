from flask import render_template, redirect, url_for
from app import app

basepath = '/'

@app.route(basepath + 'profil', methods = ['GET'])
def profil():
    metadata = {"title":"Profil", "pagename": "profil"}
    return render_template('profil.html', metadata=metadata)