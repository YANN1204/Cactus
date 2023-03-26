from flask import render_template, request, session, url_for
from flask import request
from datetime import datetime
import json

from app import app
from app.services.servicesGETData import GetDataServices
from app.services.servicesPOSTData import PostDataServices
from app.services.servicesDELETEData import DeleteDataServices
from app.services.servicesSETData import SetDataServices
from app.models.dataDAO import DataDAO 
from app.controllers.LoginController import reqlogged


dd = DataDAO()
gds = GetDataServices()
pds = PostDataServices()
dds = DeleteDataServices()
sds = SetDataServices()

file_path = "app\static\items_directus.json"
with open(file_path, 'r') as f:
    items_directus = json.load(f)

basepath = '/'


@app.route(basepath + 'fiches', methods = ['GET'])
def fiches():

    # requête données de connexion et utilisateur
    logged = session.get("logged", False)
    username = session.get("username", None)

    # requête de toutes les fiches
    data = gds.display_places(items_directus['urlac'], items_directus['urlu'], items_directus['urlact'], items_directus['urlt'], items_directus['urlr'], items_directus['urli'], items_directus['urlc'])
    
    # données statique de la page
    metadata = {"title":"Fiches", "pagename": "fiches"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}

    return render_template('fiches.html', metadata=metadata, data=data, logged=logged, username=username, images=images)


@app.route(basepath + 'research', methods=['GET'])
def research_in_cards():

    # requête données de connexion et utilisateur
    logged = session.get("logged", False)
    username = session.get("username", None)

    # requête de toutes les fiches
    data = gds.display_places(items_directus['urlac'], items_directus['urlu'], items_directus['urlact'], items_directus['urlt'], items_directus['urlr'], items_directus['urli'], items_directus['urlc'])
    
    # requête des données renseigné dans la recherche
    content_research = request.args.get('content_research')
    type_of_cards = request.args.get('type_of_cards')
    room = request.args.get('choice_room')

    # filtre des fiches alternatives en fonction des données renseigné dans la recherche
    data_filter = gds.filter(data, content_research, type_of_cards, room)

    # données statique de la page
    metadata = {"title":"Fiches", "pagename":"fiches"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}

    return render_template('fiches.html', metadata=metadata, data=data_filter, logged=logged, username=username, images=images)


@app.route('/fiche')
def fiche():

    # requête données de connexion et utilisateur
    logged = session.get("logged", False)
    username = session.get("username", None)
    idFiche = request.args.get('idFiche', None)

    # requête des données d'une fiche particulière
    data = gds.display_instance(idFiche, items_directus['urlac'], items_directus['urlu'], items_directus['urlt'], items_directus['urlact'], items_directus['urlr'], items_directus['urlc'], items_directus['urli'])
    
    # mise à jour de la base de donnée
    list_item = list(items_directus.values())
    dd.save_all_items(list_item)

    # requête de l'adoption ou non de la fiche par l'utilisateur connecté
    adopted=gds.card_adopted(idFiche,session.get("userId","0"))
    
    # données statique de la page
    metadata = {"title":"Fiche", "pagename": "fiche"}
    images = { 'left-clear-clip':url_for('static', filename="/Images/left-clear-clip.png"), 'left-dark-clip':url_for('static', filename="/Images/left-dark-clip.png"), 
              'logo-cactus':url_for('static', filename="/Images/logo-cactus.png"), 'love-earth':url_for('static', filename="/Images/love-earth.png")}
    
    return render_template('fiche.html', data = data, metadata=metadata, logged=logged, username=username, idFiche=idFiche, adopted=adopted, images=images)



@app.route('/button_click_adopt/<idFiche>')
def button_click_adopt(idFiche):
    
    # vérification de la connexion si l'utilisateur veut adopter une fiche pratique ou conseil
    if (session.get("logged", False)==False):
        metadata = {"title":"Fiches", "pagename": "fiches"}
        return render_template('login.html', metadata=metadata, provide=True)
    
    # requête données de connexion et utilisateur
    idFiche = request.args.get('idFiche')
    idUser = session.get("userId", None)
    logged = session.get("logged", False)
    username = session.get("username", None)

    #Ajout de l'id de l'utilisateur dans la table 'users_alternative_cards' 
    pds.post_data("users_alternative_cards/",{"users_id": idUser})    

    #requête des fiches d'alternative adoptées
    cardsAdoptedList = dd.get_data_Directus("users_alternative_cards")
    #obtention de l'id de l'element de la table users_alternative_cards à modifier
    idcard = str(cardsAdoptedList["data"][-1]["id"])    
    #ajout de l'id de la card
    sds.update_smt(path="users_alternative_cards",id=idcard,new_data={"alternative_cards_id":idFiche})    

    # mise à jour de la base de donnée
    list_item = list(items_directus.values())
    dd.save_all_items(list_item)

    # vérification que la fiche à été adopter
    adopted = gds.card_adopted(idFiche,session.get("userId","0"))
    # requête des données de la fiche pratique ou conseil adoptée
    data = gds.display_instance(idFiche, items_directus['urlac'], items_directus['urlu'], items_directus['urlt'], items_directus['urlact'], items_directus['urlr'], items_directus['urlc'], items_directus['urli'])
    
    #recupération des informations de l'impact
    impact_card=dd.get_data_Directus("impacts/"+data["impact"])['data']
    impact_card['impact_type']='use'
    impact_card['user_id']= idUser

    #recupération de la date courante
    now = datetime.now()
    impact_card['date_created']=now.date().isoformat()
    
    #ajout de l'impact dans la table impacts
    pds.post_data("impacts/",{'user_id' : impact_card['user_id'], 'impact_type': impact_card['impact_type'], 'impact_topic': impact_card['impact_topic'], 'sentence_on_data': impact_card['sentence_on_data'], 'numerical_data': impact_card['numerical_data'], 'unit':impact_card['unit'], 'date_created':impact_card['date_created']})
    
    # données statique de la page
    metadata = {"title":"Fiches", "pagename": "fiches"}
    images = { 'left-clear-clip':url_for('static', filename="/Images/left-clear-clip.png"), 'left-dark-clip':url_for('static', filename="/Images/left-dark-clip.png"), 
              'logo-cactus':url_for('static', filename="/Images/logo-cactus.png"), 'love-earth':url_for('static', filename="/Images/love-earth.png")}
    
    return render_template('fiche.html', metadata=metadata, adopted=adopted, data=data, logged=logged ,username=username, idFiche=idFiche, images=images)


@app.route('/button_click_unadopt/<idFiche>')
def button_click_unadopt(idFiche):

    # vérification de la connexion si l'utilisateur ne veut plus adopter une fiche pratique ou conseil
    if (session.get("logged", False)==False):
        metadata = {"title":"Fiches", "pagename": "fiches"}
        return render_template('login.html', metadata=metadata)

    # requête données de connexion et utilisateur
    idFiche = request.args.get('idFiche')
    idUser = session.get("userId", "0")
    logged = session.get("logged", False)
    username = session.get("username", None)

    # désadopter la fiche dans la base de donnée pour l'utilisateur
    index = gds.index_users_alternative_cards(idFiche=idFiche,idUser=idUser)
    index= str(index)
    dds.unadopt_card(index=index)

    #suppression de l'impact
    #recupération de la date courante au format iso8601
    now = datetime.now()
    date_end = now.date().isoformat()
    #récupération de l'id de l'impact dans la table impacts
    idImpact=gds.index_impact(idFiche=idFiche,idUser=idUser)
    sds.update_smt(path='impacts', id=idImpact, new_data={'date_end': date_end })
    
    # mise à jour de la base de donnée
    list_item = list(items_directus.values())
    dd.save_all_items(list_item)
    
    # requête des données de la fiche
    data = gds.display_instance(idFiche, items_directus['urlac'], items_directus['urlu'], items_directus['urlt'], items_directus['urlact'], items_directus['urlr'], items_directus['urlc'], items_directus['urli'])

    # vérification que la fiche à été adopter
    adopted=gds.card_adopted(idFiche,session.get("userId","0"))

    # données statique de la page
    metadata = {"title":"Fiches", "pagename": "fiches"}
    images = { 'left-clear-clip':url_for('static', filename="/Images/left-clear-clip.png"), 'left-dark-clip':url_for('static', filename="/Images/left-dark-clip.png"), 
              'logo-cactus':url_for('static', filename="/Images/logo-cactus.png"), 'love-earth':url_for('static', filename="/Images/love-earth.png")}
    
    return render_template('fiche.html',  metadata=metadata, adopted=adopted, data=data, logged=logged ,username=username, idFiche=idFiche, images=images)


@app.route(basepath + 'postCard', methods=['POST'])
@reqlogged
def com_card():

    # requête des données pour poster le commentaire
    text_com = request.form.get("com")
    id_card = request.form.get("id-card")
    com_radio = request.form.get("comRadio")
    newData = {
        "text": text_com,
        "user_id": session["id"],
        "comment_type": com_radio,
        "alternative_card_id": id_card,
    }

    # Post du commentaire 
    data = pds.post_data('comments', data=newData)

    # mise à jour de la base de donnée pour voir le nouveau commentaire
    list_item = list(items_directus.values())
    dd.save_all_items(list_item)

    # requête des données de la fiche
    data = gds.display_instance(id_card, items_directus['urlac'], items_directus['urlu'], items_directus['urlt'], items_directus['urlact'], items_directus['urlr'], items_directus['urlc'], items_directus['urli'])
    
    metadata = {"title":"Fiche", "pagename": "Fiche"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}

    return render_template('fiche.html', metadata=metadata, data=data, images=images)


@app.route('/fiches', methods=['GET', 'POST'])
def handle_button_click():

    # Fonctionnalité non généralisé
    data = {"status":"draft","title":"Test","room_id":"032160c4-caa2-451f-b3c8-72c53360345f"}
    collection = 'alternative_cards'
    pds.post_data(collection, data)
    metadata = {"title":"Fiches", "pagename": "fiches"}

    return render_template('fiches.html', metadata=metadata)
