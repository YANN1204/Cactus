from flask import render_template, session
from app import app

basepath = '/'

@app.route(basepath + 'jeux', methods = ['GET'])
def jeux():
    is_connected = session.get("is_connected", False)
    id_user = session.get("id_user", None)
    metadata = {"title":"Jeux", "pagename": "jeux"}
    return render_template('jeux.html', metadata=metadata, is_connected=is_connected, id_user=id_user)