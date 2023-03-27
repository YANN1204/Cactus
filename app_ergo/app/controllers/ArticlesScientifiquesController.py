from flask import render_template, session, url_for

from app import app

basepath = '/'

@app.route(basepath + 'articles_scientifiques', methods = ['GET'])
def articles_scientifiques():
    
    # requête données de connexion et utilisateur
    logged = session.get("logged", False)
    id_user = session.get("id_user", None)

    # données statique de la page
    metadata = {"title":"Articles scientifiques", "pagename": "articles scientifiques"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}

    return render_template('articles_scientifiques.html', metadata=metadata, logged=logged, id_user=id_user, images=images)