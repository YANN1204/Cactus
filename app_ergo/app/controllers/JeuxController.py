from flask import render_template, redirect, url_for
from app import app

basepath = '/'

@app.route(basepath + 'jeux', methods = ['GET'])
def jeux():
    metadata = {"title":"Jeux", "pagename": "jeux"}
    return render_template('jeux.html', metadata=metadata)