from flask import render_template, request, session
from app import app
from app.services.servicesGETData import GetDataServices
from app.models.dataDAO import DataDAO

app.secret_key = "secret_key"

dd = DataDAO()
gds = GetDataServices()
basepath = '/'

list_item = ['alternative_cards', 'alternative_cards_tags', 'comments', 'forums', 'forums_tags', 'impacts',
             'rooms', 'tags', 'users', 'users_alternative_cards', 'users_tags']

urlac = "alternative_cards"
urlf = "forums"
urlimp = "impacts"
urlu = "users"
urlt = "tags"
urlft = "forums_tags"
urlact = "alternative_cards_tags"
urlr = "rooms"
urlc = "comments"


@app.route(basepath, methods = ['GET'])
def accueil():
    session["is_connected"] = False
    is_connected = session.get("is_connected", False)
    data={}
    metadata = {"title": "Accueil", "pagename": "accueil_guest"}
    data["impact"] = int(gds.display_impact(url=urlimp,impacttype="1"))
    data["impact_now"] = gds.display_impact_now()
        
    return render_template('accueil_guest.html', metadata=metadata, data=data, is_connected=is_connected)


@app.route(basepath + 'connexion', methods = ['GET', 'POST'])
def connexion():
    is_connected = session.get("is_connected", False)
    email = request.form.get("email")
    password = request.form.get("password")
    print(email)
    print(password)
    data_users = dd.get_data(urlu)
    metadata = {"title": "Accueil", "pagename": "accueil"}

    for i in data_users:
        if i['mail'] == email and i['password'] == password:
            data={}
            session["is_connected"] = True
            is_connected = True  # set is_connected to True
            data["impact"] = int(gds.display_impact(url=urlimp,impacttype="1"))
            data["impact_now"] = gds.display_impact_now()
            return render_template('accueil.html', metadata=metadata, data=data, is_connected=is_connected)
        else:
            data = "Aucun compte reconnu, créez-vous en un !"
            return render_template('login.html', metadata=metadata, data=data, is_connected=is_connected)


@app.route(basepath + 'accueil', methods = ['GET'])
def accueil_connected():
    is_connected = session.get("is_connected", False)
    data={}
    metadata = {"title": "Accueil", "pagename": "accueil"}
    data["impact"] = int(gds.display_impact(url=urlimp,impacttype="1"))
    data["impact_now"] = gds.display_impact_now()
        
    return render_template('accueil.html', metadata=metadata, data=data, is_connected=is_connected)


@app.route(basepath + 'research_accueil', methods=['GET'])
def research_accueil():
    is_connected = session.get("is_connected", False)
    cards_and_forums = {}
    data_cards = gds.display_places(urlac, urlu, urlact, urlt, urlr)
    data_forums = gds.display_places(urlf, urlu, urlft, urlt, urlr)
    content_research = request.args.get('content_research')
    cards_and_forums['cards'] = data_cards
    cards_and_forums['forums'] = data_forums

    cards_and_forums['cards'] = gds.filter(data_cards, content_research)
    cards_and_forums['forums'] = gds.filter(data_forums, content_research)

    metadata = {"title":"Accueil", "pagename":"accueil"}
    return render_template('accueil_research.html', metadata=metadata, data=cards_and_forums, is_connected=is_connected)


@app.route(basepath + 'deconnexion', methods = ['GET', 'POST'])
def deconnexion():
    is_connected = session.get("is_connected", False)
    session["is_connected"] = False
    is_connected = False  # set is_connected to True
    data={}
    metadata = {"title": "Accueil", "pagename": "accueil"}
    data["impact"] = int(gds.display_impact(url=urlimp,impacttype="1"))
    data["impact_now"] = gds.display_impact_now()
        
    return render_template('accueil_guest.html', metadata=metadata, data=data, is_connected=is_connected)



