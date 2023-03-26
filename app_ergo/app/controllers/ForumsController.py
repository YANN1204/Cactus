from flask import render_template, request, session, url_for
import json

from app import app
from app.services.servicesPOSTData import PostDataServices
from app.services.servicesGETData import GetDataServices
from app.controllers.LoginController import reqlogged
from app.models.dataDAO import DataDAO 

gds = GetDataServices()
pds = PostDataServices()
dd = DataDAO()

file_path = "app\static\items_directus.json"
with open(file_path, 'r') as f:
    items_directus = json.load(f)

basepath = '/'

@app.route(basepath + 'forums', methods = ['GET'])
@reqlogged
def forums():

    # requête données de connexion et utilisateur
    logged = session.get("logged", False)
    username = session.get("username", None)

    # requête des données des forums
    data = gds.display_places(items_directus['urlf'], items_directus['urlu'], items_directus['urlft'], items_directus['urlt'], items_directus['urlr'], items_directus['urli'], items_directus['urlc'])
    
    # données statique de la page
    metadata = {"title":"Forums", "pagename": "forums"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}

    return render_template('forums.html', data=data, metadata=metadata, logged=logged, username=username, images=images)


@app.route(basepath + 'research_forums', methods=['GET'])
def research_in_forums():

    # requête données de connexion et utilisateur
    logged = session.get("logged", False)
    username = session.get("username", None)

    # requête des données des forums
    data = gds.display_places(items_directus['urlf'], items_directus['urlu'], items_directus['urlft'], items_directus['urlt'], items_directus['urlr'], items_directus['urli'], items_directus['urlc'])
    
    # requête des données renseigné dans la recherche
    content_research = request.args.get('content_research')

    # filtre des forums en fonction des données renseigné dans la recherche
    data_filter = gds.filter(data, content_research, "forum", "maison entiere")

    # données statique de la page
    metadata = {"title":"Forums", "pagename":"forums"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}

    return render_template('forums.html', metadata=metadata, data=data_filter, username=username, logged=logged, images=images)


@app.route(basepath + 'forum')
def forum():

    # requête données de connexion et utilisateur
    logged = session.get("logged", False)
    username = session.get("username", None)
    idForum = request.args.get('idForum', None)

    # date du jour
    today = gds.date_today()

    # requête des données du forum particulier
    data = gds.display_instance(idForum, items_directus['urlf'], items_directus['urlu'], items_directus['urlt'], items_directus['urlft'], items_directus['urlr'], items_directus['urlc'], items_directus['urli'])
    
    # données statique de la page
    metadata = {"title":"Forum", "pagename": "forum"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}

    return render_template('forum.html', data = data, metadata=metadata, logged=logged, username=username, images=images, today=today)


@app.route(basepath + 'postForum', methods=['POST'])
@reqlogged
def com_forum():

    # requête des données pour poster le commentaire
    text_com = request.form.get("com")
    id_forum = request.form.get("id-forum")
    if request.form.get("id-com"):
        id_com = request.form.get("id-com")
    else :
        id_com = None
    newData = {
        "text": text_com,
        "user_id": session["userId"],
        "text": text_com,
        "forum_id": id_forum,
        "comment_subject": id_com
    }

    # Post du commentaire 
    pds.post_data('comments', data=newData)

     # mise à jour de la base de donnée pour voir le nouveau commentaire
    list_item = list(items_directus.values())    
    dd.save_all_items(list_item)

    # requête des données du forum
    data = gds.display_instance(id_forum, items_directus['urlf'], items_directus['urlu'], items_directus['urlt'], items_directus['urlft'], items_directus['urlr'], items_directus['urlc'], items_directus['urli'])
    
    # données statique de la page
    metadata = {"title":"Forum", "pagename": "Forum"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}

    return render_template('forum.html', metadata=metadata, data=data, images=images)