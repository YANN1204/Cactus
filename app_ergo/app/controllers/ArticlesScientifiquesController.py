from flask import render_template, redirect, url_for
from app import app

basepath = '/'

@app.route(basepath + 'articles_scientifiques', methods = ['GET'])
def articles_scientifiques():
    metadata = {"title":"Articles_scientifiques", "pagename": "articles_scientifiques"}
    print(metadata['pagename'])
    return render_template('articles_scientifiques.html', metadata=metadata)