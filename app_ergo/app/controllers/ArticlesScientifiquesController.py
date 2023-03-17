from flask import render_template, session
from app import app

basepath = '/'

@app.route(basepath + 'articles_scientifiques', methods = ['GET'])
def articles_scientifiques():
    is_connected = session.get("is_connected", False)
    id_user = session.get("id_user", None)
    metadata = {"title":"Articles_scientifiques", "pagename": "articles_scientifiques"}
    return render_template('articles_scientifiques.html', metadata=metadata, is_connected=is_connected, id_user=id_user)