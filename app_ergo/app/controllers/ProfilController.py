from flask import render_template, session
from app import app

basepath = '/'

@app.route(basepath + 'profil', methods = ['GET'])
def profil():
    is_connected = session.get("is_connected", False)
    print(is_connected)
    metadata = {"title":"Profil", "pagename": "profil"}
    return render_template('profil.html', metadata=metadata, is_connected=is_connected)