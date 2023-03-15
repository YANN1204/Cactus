from flask import render_template, request, session
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
# les noms des différentes collection associées à l'item qui nous
# intéresse ici (fiche)

url_item = "alternative_cards"
urlu = "users"
urlt = "tags"
urlact = "alternative_cards_tags"
urlr = "rooms"
urlc = "comments"

@app.route(basepath + 'fiches', methods = ['GET'])
def fiches():
    is_connected = session.get("is_connected", False)
    print(is_connected)
    data = gds.display_places(url_item, urlu, urlact, urlt, urlr)
    metadata = {"title":"Fiches", "pagename": "fiches"}
    return render_template('fiches.html', metadata=metadata, data=data, is_connected=is_connected)

@app.route(basepath + 'research', methods=['GET'])
def research_in_cards():
    is_connected = session.get("is_connected", False)
    data = gds.display_places(url_item, urlu, urlact, urlt, urlr)
    content_research = request.args.get('content_research')
    data_filter = gds.filter(data, content_research)
    metadata = {"title":"Fiches", "pagename":"fiches"}
    return render_template('fiches.html', metadata=metadata, data=data_filter, is_connected=is_connected)


@app.route('/fiche')
def fiche():
    is_connected = session.get("is_connected", False)
    idFiche = request.args.get('idFiche', None)
    data = gds.display_instance(idFiche, url_item, urlu, urlt, urlact, urlr, urlc)
    metadata = {"title":"Fiche", "pagename": "fiche"}
    return render_template('fiche.html', data = data, metadata=metadata, is_connected=is_connected)

@app.route('/fiches', methods=['GET', 'POST'])
def handle_button_click():
    # Appel de votre fonction Python
    data = {"status":"draft","title":"Test","room_id":"032160c4-caa2-451f-b3c8-72c53360345f"}
    collection = 'alternative_cards'
    pds.post_data(collection, data)
    metadata = {"title":"Fiches", "pagename": "fiches"}
    return render_template('fiches.html', metadata=metadata)

@app.route('/monbouton_2', methods=['GET', 'DELETE'])
def button_click_delete():
    # Appel de votre fonction delete python
    card = gds.alternative_by_title(basepath + "alternative_cards", "Test2")
    id = card['id']
    collection = "alternative_cards"
    message = dds.delete_cards(collection, id)
    metadata = {"title":"Fiches", "pagename": "fiches"}
    return render_template('fiches.html', metadata=metadata)

@app.route('/monbouton_3', methods=['GET', 'SET'])
def button_click_set():
    # Appel de votre fonction set python
    card = gds.alternative_by_title(basepath + "alternative_cards", "Test")
    id = card['id']
    new_data={"title":"Test2"}
    collection = "alternative_cards"
    message = sds.update_card(collection, new_data, id)
    print (message)
    metadata = {"title":"Fiches", "pagename": "fiches"}
    return render_template('fiches.html', metadata=metadata)
