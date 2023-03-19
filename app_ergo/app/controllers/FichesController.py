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
    logged = session.get("logged", False)
    username = session.get("username", None)
    data = gds.display_places(url_item, urlu, urlact, urlt, urlr)
    metadata = {"title":"Fiches", "pagename": "fiches"}
    return render_template('fiches.html', metadata=metadata, data=data, logged=logged, username=username)

@app.route(basepath + 'research', methods=['GET'])
def research_in_cards():
    logged = session.get("logged", False)
    username = session.get("username", None)
    data = gds.display_places(url_item, urlu, urlact, urlt, urlr)
    content_research = request.args.get('content_research')
    data_filter = gds.filter(data, content_research)
    metadata = {"title":"Fiches", "pagename":"fiches"}
    return render_template('fiches.html', metadata=metadata, data=data_filter, logged=logged, username=username)


@app.route('/fiche')
def fiche():
    logged = session.get("logged", False)
    username = session.get("username", None)
    idFiche = request.args.get('idFiche', None)
    data = gds.display_instance(idFiche, url_item, urlu, urlt, urlact, urlr, urlc)
    
    metadata = {"title":"Fiche", "pagename": "fiche"}
    return render_template('fiche.html', data = data, metadata=metadata, logged=logged, username=username)


# Route pour indiquer à la base de donnée qu'un utilisateur à adopté une fiche (qui n'est pas fini je crois)
@app.route('/ficheAdopt')
def button_click_adopt():
    username = session.get("username", False)
    logged = session.get("logged", None)
    idFiche = "25b2f9dc-6a13-4b0b-ad21-ee1e0d7d3043"
    idUsers = "eca95393-2325-45e5-bacb-bf0c59285fad"
    ##du coup ca marche pas j'arrive pas à rentrer les bon id.
    ##enfin les numéros enregistrer dans "alternative_card_adopted" c'est pas les id des fiches...
    new_data = {"alternative_card_adopted": [3, 4,]}
    metadata = {"title":"Fiche", "pagename": "fiche"}
    sds.update_smt(urlu, id=idUsers, new_data=new_data, metadata=metadata, username=username, logged=logged)

    
    metadata = {"title":"Fiches", "pagename": "fiches"}
    #retourn un pop up "c'est ok"
    return render_template('fiches.html', metadata=metadata)


# Route pour poster une fiche qui n'est pas fini je crois
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
