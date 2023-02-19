from flask import render_template, redirect, url_for
from app import app
from app.services.servicesPostData import PostDataServices
from app.services.servicesPostData import PostDataServices

pds = PostDataServices()

basepath = '/'

@app.route(basepath + 'fiches', methods = ['GET'])
def fiches():
    metadata = {"title":"Fiches", "pagename": "fiches"}
    return render_template('fiches.html', metadata=metadata)

@app.route('/mon-bouton', methods=['POST'])
def handle_button_click():
    # Appel de votre fonction Python
    pds.post_cards()
    metadata = {"title":"Fiches", "pagename": "fiches"}
    return render_template('fiches.html', metadata=metadata)