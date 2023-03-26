from flask import render_template, request, session, url_for
import json

from app import app
from app.services.servicesGETData import GetDataServices
from app.models.dataDAO import DataDAO
from app.controllers.LoginController import reqlogged

app.secret_key = "secret_key"

dd = DataDAO()
gds = GetDataServices()
basepath = '/'

file_path = "app\static\items_directus.json"
with open(file_path, 'r') as f:
    items_directus = json.load(f)


@app.route(basepath, methods = ['GET'])
def accueil():

    # requête données de connexion et utilisateur
    logged = session.get("logged", False)
    username = session.get("username", None)

    # requête données impact communauté
    data={}
    data['tot_impacts'] = gds.impact_total_sum(items_directus['urli'])
    data['impact_per_month'] = gds.impact_per_month(items_directus['urli'])

    # données statique de la page
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}
    metadata = {"title": "Accueil", "pagename": "accueil_guest"}
        
    return render_template('accueil_guest.html', metadata=metadata, data=data, logged=logged, username=username, images=images)


@app.route(basepath + 'accueil', methods = ['GET'])
@reqlogged
def accueil_connected():

    # requête données de connexion et utilisateur
    logged = session.get("logged", False)
    username = session.get("username", None)
    session["logged"] = logged
    session['username'] = username

    # requête données impact communauté et user
    data={}
    data['tot_impacts'] = gds.impact_total_sum(items_directus['urli'])
    data['impact_per_month'] = gds.impact_per_month(items_directus['urli'])
    data["impact_user"] = gds.impact_total_sum(items_directus['urli'], id = session['userId'])

    # données statique de la page
    metadata = {"title": "Accueil", "pagename": "accueil"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}
        
    return render_template('accueil.html', metadata=metadata, data=data, logged=logged, username=username, images=images)


@app.route(basepath + 'research_accueil', methods=['GET'])
def research_accueil():

    # requête données de connexion et utilisateur
    logged = session.get("logged", False)
    username = session.get("username", None)

    # requête de toutes les fiches d'alternative et des forums
    cards_and_forums = {}
    data_cards = gds.display_places(items_directus['urlac'], items_directus['urlu'], items_directus['urlact'], items_directus['urlt'], items_directus['urlr'], items_directus['urli'], items_directus['urlc'])
    data_forums = gds.display_places(items_directus['urlf'], items_directus['urlu'], items_directus['urlft'], items_directus['urlt'], items_directus['urlr'], items_directus['urli'], items_directus['urlc'])
    
    # requête des données renseigné dans la recherche
    content_research = request.args.get('content_research')
    type_of_data = request.args.get('type_of_data')
    room = request.args.get('room')

    # filtre des fiches alternatives en fonction des données renseigné dans la recherche
    cards_and_forums['cards'] = data_cards
    cards_and_forums['cards'] = gds.filter(data_cards, content_research, type_of_data, room)

    # filtre des forums en fonction des données renseigné dans la recherche
    if type_of_data == '4' or type_of_data == "Tous":
        cards_and_forums['forums'] = data_forums
        type_of_data = "forum"
        cards_and_forums['forums'] = gds.filter(data_forums, content_research,type_of_data, room)

    # données statique de la page
    metadata = {"title":"Accueil", "pagename":"accueil"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}

    return render_template('accueil_research.html', metadata=metadata, data=cards_and_forums, logged=logged, username=username, images=images)



