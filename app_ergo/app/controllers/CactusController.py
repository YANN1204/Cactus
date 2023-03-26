from flask import render_template, session, url_for

from app import app

basepath = '/'

@app.route(basepath + 'cactus', methods = ['GET'])
def cactus():

    # requête données de connexion et utilisateur
    logged = session.get("logged", False)
    username = session.get("username", None)

    # données statique de la page
    metadata = {"title":"Cactus", "pagename": "cactus"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}

    return render_template('cactus.html', metadata=metadata, username=username, logged=logged, images=images)