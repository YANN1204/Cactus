from flask import render_template, session
from app import app

basepath = '/'

@app.route(basepath + 'jeux', methods = ['GET'])
def jeux():
    logged = session.get("logged", False)
    username = session.get("username", None)
    metadata = {"title":"Jeux", "pagename": "jeux"}
    return render_template('jeux.html', metadata=metadata, logged=logged, username=username)