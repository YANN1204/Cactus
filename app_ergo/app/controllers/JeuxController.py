from flask import render_template, session, url_for

from app import app

basepath = '/'

@app.route(basepath + 'jeux', methods = ['GET'])
def jeux():

    # requête données de connexion et utilisateur
    logged = session.get("logged", False)
    username = session.get("username", None)

    # données statique de la page
    metadata = {"title":"Jeux", "pagename": "jeux"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}
    
    return render_template('jeux.html', metadata=metadata, logged=logged, username=username, images=images)