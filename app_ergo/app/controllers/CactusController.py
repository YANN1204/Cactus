from flask import render_template, session
from app import app

basepath = '/'

@app.route(basepath + 'cactus', methods = ['GET'])
def cactus():
    is_connected = session.get("is_connected", False)
    id_user = session.get("id_user", None)
    metadata = {"title":"Cactus", "pagename": "cactus"}
    return render_template('cactus.html', metadata=metadata, is_connected=is_connected, id_user=id_user)