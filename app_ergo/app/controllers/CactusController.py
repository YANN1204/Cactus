from flask import render_template, redirect, url_for
from app import app

basepath = '/'

@app.route(basepath + 'cactus', methods = ['GET'])
def cactus():
    metadata = {"title":"Cactus", "pagename": "cactus"}
    return render_template('cactus.html', metadata=metadata)