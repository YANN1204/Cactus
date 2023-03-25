from flask import render_template, request, session, redirect, url_for, flash
from app import app
from app.services.servicesGETData import GetDataServices
from app.models.dataDAO import DataDAO
from app.controllers.LoginController import reqlogged

app.secret_key = "secret_key"

dd = DataDAO()
gds = GetDataServices()
basepath = '/'

urlac = "alternative_cards"
urlf = "forums"
urlimp = "impacts"
urlu = "users"
urlt = "tags"
urlft = "forums_tags"
urlact = "alternative_cards_tags"
urlr = "rooms"
urlc = "comments"
urli = "impacts"


@app.route(basepath, methods = ['GET'])
def accueil():
    logged = session.get("logged", False)
    username = session.get("username", None)
    data={}
    metadata = {"title": "Accueil", "pagename": "accueil_guest"}
    data["impact"] = int(gds.display_impact(url=urlimp,impacttype="1"))
    data["impact_now"] = gds.display_impact_now()
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}
        
    return render_template('accueil_guest.html', metadata=metadata, data=data, logged=logged, username=username, images=images)


@app.route(basepath + 'accueil', methods = ['GET'])
@reqlogged
def accueil_connected():
    logged = session.get("logged", False)
    username = session.get("username", None)
    session["logged"] = logged
    session['username'] = username
    data={}
    metadata = {"title": "Accueil", "pagename": "accueil"}
    data["impact"] = int(gds.display_impact(url=urlimp,impacttype="1"))
    data["impact_now"] = gds.display_impact_now()
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}
        
    return render_template('accueil.html', metadata=metadata, data=data, logged=logged, username=username, images=images)


@app.route(basepath + 'research_accueil', methods=['GET'])
def research_accueil():
    logged = session.get("logged", False)
    username = session.get("username", None)
    cards_and_forums = {}
    data_cards = gds.display_places(urlac, urlu, urlact, urlt, urlr)
    data_forums = gds.display_places(urlf, urlu, urlft, urlt, urlr)
    content_research = request.args.get('content_research')
    cards_and_forums['cards'] = data_cards
    cards_and_forums['forums'] = data_forums

    cards_and_forums['cards'] = gds.filter(data_cards, content_research)
    cards_and_forums['forums'] = gds.filter(data_forums, content_research)

    metadata = {"title":"Accueil", "pagename":"accueil"}
    return render_template('accueil_research.html', metadata=metadata, data=cards_and_forums, logged=logged, username=username)



