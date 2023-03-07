from flask import render_template, redirect, url_for
from app import app
from app.services.servicesGETData import GetDataServices
from app.services.servicesPOSTData import PostDataServices
from app.services.servicesDELETEData import DeleteDataServices
from app.services.servicesSETData import SetDataServices

gds = GetDataServices()
pds = PostDataServices()
dds = DeleteDataServices()
sds = SetDataServices()

basepath = '/'

@app.route(basepath + 'fiches', methods = ['GET'])
def fiches():
    metadata = {"title":"Fiches", "pagename": "fiches"}
    return render_template('fiches.html', metadata=metadata)

@app.route('/fiches', methods=['GET', 'POST'])
def handle_button_click():
    # Appel de votre fonction Python
    pds.post_cards()
    metadata = {"title":"Fiches", "pagename": "fiches"}
    return render_template('fiches.html', metadata=metadata)

@app.route('/monbouton_2', methods=['GET', 'DELETE'])
def button_click_delete():
    # Appel de votre fonction delete python
    card = gds.alternative_by_title(basepath + "alternative_cards", "Test2")
    id = card['id']
    message = dds.delete_cards(id)
    metadata = {"title":"Fiches", "pagename": "fiches"}
    return render_template('fiches.html', metadata=metadata)

@app.route('/monbouton_3', methods=['GET', 'SET'])
def button_click_set():
    # Appel de votre fonction set python
    card = gds.alternative_by_title(basepath + "alternative_cards", "Test")
    id = card['id']
    message = sds.update_card(id)
    print (message)
    metadata = {"title":"Fiches", "pagename": "fiches"}
    return render_template('fiches.html', metadata=metadata)