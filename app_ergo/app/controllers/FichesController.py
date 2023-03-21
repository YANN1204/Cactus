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


@app.route('/ficheAdopt')
def button_click_adopt():
    #il manque a réussir a recupérer l'id courant de la fiche qui est deja dans l'url mais je sais pas comment faire ..
    #et aussi recuperer l'id de l'user mais ca on va bientot le terminer
    idFiche = "298d5868-37c4-41fd-bad8-5b0b1b9ccd66"
    idUsers = "eca95393-2325-45e5-bacb-bf0c59285fad"  
    #Ajout de l'id de l'user dans la table users_alternative_cards 
    pds.post_data("users_alternative_cards/",{"users_id": idUsers})    
    #récupération du nb d'element dans la table users_alternative_cards
    ###remplacer get data par get instance pour modifier les alternative adopter à la ligne 59 de servicesGETData.py
    cardsList=gds.display_data("users_alternative_cards/")
    #obtention de l'id de l'element de la table users_alternative_cards à modifier
    idcard=str(cardsList["data"][-1]["id"])
    #ajout de l'id de la card
    sds.update_smt(path="users_alternative_cards",id=idcard,new_data={"alternative_cards_id":idFiche})

    metadata = {"title":"Fiches", "pagename": "fiches"}
    #retourn un pop up "c'est ok"
    return render_template('fiches.html', metadata=metadata)

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
