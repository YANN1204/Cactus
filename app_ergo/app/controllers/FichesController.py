from flask import flash, render_template, request, session, url_for
from flask import request
from app import app
from app.services.servicesGETData import GetDataServices
from app.services.servicesPOSTData import PostDataServices
from app.services.servicesDELETEData import DeleteDataServices
from app.services.servicesSETData import SetDataServices
from app.models.dataDAO import DataDAO 
from app.controllers.LoginController import reqlogged
import datetime
from datetime import datetime


dd = DataDAO()
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
urli = "impacts"

@app.route(basepath + 'fiches', methods = ['GET'])
def fiches():
    logged = session.get("logged", False)
    username = session.get("username", None)
    data = gds.display_places(url_item, urlu, urlact, urlt, urlr)
    metadata = {"title":"Fiches", "pagename": "fiches"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}
    return render_template('fiches.html', metadata=metadata, data=data, logged=logged, username=username, images=images)

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
       
    data = gds.display_instance(idFiche, url_item, urlu, urlt, urlact, urlr, urlc, urli)
    # import de la base de donnée
    list_item = ['alternative_cards', 'alternative_cards_tags', 'comments', 'forums', 'forums_tags', 'impacts','rooms', 'tags', 'users', 'users_alternative_cards', 'users_tags']
    dd = DataDAO()
    dd.save_all_items(list_item)
    adopted=gds.card_adopted(idFiche,session.get("userId","0"))
    
    data = gds.display_instance(idFiche, url_item, urlu, urlt, urlact, urlr, urlc, urli)
    metadata = {"title":"Fiche", "pagename": "fiche"}
    images = { 'left-clear-clip':url_for('static', filename="/Images/left-clear-clip.png"), 'left-dark-clip':url_for('static', filename="/Images/left-dark-clip.png"), 
              'logo-cactus':url_for('static', filename="/Images/logo-cactus.png"), 'love-earth':url_for('static', filename="/Images/love-earth.png")}
    return render_template('fiche.html', data = data, metadata=metadata, logged=logged, username=username, idFiche=idFiche, adopted=adopted, images=images)



@app.route('/button_click_adopt/<idFiche>')
def button_click_adopt(idFiche):
    
    if (session.get("logged", False)==False):
        metadata = {"title":"Fiches", "pagename": "fiches"}
        return render_template('login.html', metadata=metadata, provide=True)
    
    idFiche = request.args.get('idFiche')
    print(idFiche)
    idUser = session.get("userId", None)
    #Ajout de l'id de l'user dans la table users_alternative_cards 
    pds.post_data("users_alternative_cards/",{"users_id": idUser})    
    dd = DataDAO()
    cardsAdoptedList=dd.get_dataInDirectus("users_alternative_cards")
    #obtention de l'id de l'element de la table users_alternative_cards à modifier
    idcard=str(cardsAdoptedList["data"][-1]["id"])    
    #ajout de l'id de la card
    sds.update_smt(path="users_alternative_cards",id=idcard,new_data={"alternative_cards_id":idFiche})    
    metadata = {"title":"Fiches", "pagename": "fiches"}
    # import de la base de donnée
    list_item = ['alternative_cards', 'alternative_cards_tags', 'comments', 'forums', 'forums_tags', 'impacts','rooms', 'tags', 'users', 'users_alternative_cards', 'users_tags']
    dd = DataDAO()
    dd.save_all_items(list_item)
    adopted=gds.card_adopted(idFiche,session.get("userId","0"))
    #recupération des informations de l'impact
    data = gds.display_instance(idFiche, url_item, urlu, urlt, urlact, urlr, urlc, urli)
    impact_card=dd.get_dataInDirectus("impacts/"+data["impact"])['data']

    impact_card['impact_type']='use'
    impact_card['user_id']= idUser

    #recupération de la date courante
    now = datetime.now()
    impact_card['date_created']=now.date().isoformat()
    
    #ajout de l'impact dans la table impacts
    pds.post_data("impacts/",{'user_id' : impact_card['user_id'], 'impact_type': impact_card['impact_type'], 'impact_topic': impact_card['impact_topic'], 'sentence_on_data': impact_card['sentence_on_data'], 'numerical_data': impact_card['numerical_data'], 'unit':impact_card['unit'], 'date_created':impact_card['date_created']})
    # Ajoutez une variable de contexte pour indiquer que la fiche a été adoptée    
    logged = session.get("logged", False)
    username = session.get("username", None)
    images = { 'left-clear-clip':url_for('static', filename="/Images/left-clear-clip.png"), 'left-dark-clip':url_for('static', filename="/Images/left-dark-clip.png"), 
              'logo-cactus':url_for('static', filename="/Images/logo-cactus.png"), 'love-earth':url_for('static', filename="/Images/love-earth.png")}
    return render_template('fiche.html', metadata=metadata, adopted=adopted, data=data, logged=logged ,username=username, idFiche=idFiche, images=images)

@app.route('/button_click_unadopt/<idFiche>')
def button_click_unadopt(idFiche):
    if (session.get("logged", False)==False):
        metadata = {"title":"Fiches", "pagename": "fiches"}
        return render_template('login.html', metadata=metadata)    
    idFiche = request.args.get('idFiche')
    idUser = session.get("userId", "0")
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
    metadata = {"title":"Fiches", "pagename": "fiches"}
    # import de la base de donnée
    list_item = ['alternative_cards', 'alternative_cards_tags', 'comments', 'forums', 'forums_tags', 'impacts','rooms', 'tags', 'users', 'users_alternative_cards', 'users_tags']
    dd = DataDAO()
    dd.save_all_items(list_item)
    data = gds.display_instance(idFiche, url_item, urlu, urlt, urlact, urlr, urlc, urli)
    logged = session.get("logged", False)
    username = session.get("username", None)
    adopted=gds.card_adopted(idFiche,session.get("userId","0"))
    images = { 'left-clear-clip':url_for('static', filename="/Images/left-clear-clip.png"), 'left-dark-clip':url_for('static', filename="/Images/left-dark-clip.png"), 
              'logo-cactus':url_for('static', filename="/Images/logo-cactus.png"), 'love-earth':url_for('static', filename="/Images/love-earth.png")}
    return render_template('fiche.html',  metadata=metadata, adopted=adopted, data=data, logged=logged ,username=username, idFiche=idFiche, images=images)


@app.route(basepath + 'postCard', methods=['POST'])
@reqlogged
def com_card():
    text_com = request.form.get("com")
    id_card = request.form.get("id-card")
    com_radio = request.form.get("comRadio")
    newData = {
        "text": text_com,
        "user_id": session["id"],
        "comment_type": com_radio,
        "alternative_card_id": id_card,
    }
    metadata = {"title":"Fiche", "pagename": "Fiche"}
    data = pds.post_data('comments', data=newData)
    # on retélécharge le json pour voir le nouveau commentaire
    list_item = ['alternative_cards', 'alternative_cards_tags', 'comments', 'forums', 'forums_tags', 'impacts',
             'rooms', 'tags', 'users', 'users_alternative_cards', 'users_tags']
    dd.save_all_items(list_item)
    # afficher fiche avec nouveau com --> à corriger
    data = gds.display_instance(id_card, url_item, urlu, urlt, urlact, urlr, urlc, urli)
    return render_template('fiche.html', metadata=metadata, data=data)


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
