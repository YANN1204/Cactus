from flask import render_template, session
from app import app

basepath = '/'

@app.route(basepath + 'cactus', methods = ['GET'])
def cactus():
    logged = session.get("logged", False)
    username = session.get("username", None)
    metadata = {"title":"Cactus", "pagename": "cactus"}
    return render_template('cactus.html', metadata=metadata, username=username, logged=logged)