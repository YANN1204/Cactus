from flask import Flask, render_template, request, session, url_for
from app import app

from app.services.servicesPOSTData import PostDataServices
from app.services.servicesGETData import GetDataServices
from app.controllers.LoginController import reqlogged
from app.models.dataDAO import DataDAO 

gds = GetDataServices()
pds = PostDataServices()
dd = DataDAO()


basepath = '/'
# les noms des différentes collection associées à l'item qui nous
# intéresse ici (forum)
url_item = "forums"
urlu = "users"
urlt = "tags"
urlft = "forums_tags"
urlr = "rooms"
urlc = "comments"
urli = "impacts"


@app.route(basepath + 'forums', methods = ['GET'])
@reqlogged
def forums():
    logged = session.get("logged", False)
    username = session.get("username", None)
    data = gds.display_places(url_item, urlu, urlft, urlt, urlr, urli, urlc)
    metadata = {"title":"Forums", "pagename": "forums"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}
    return render_template('forums.html', data=data, metadata=metadata, logged=logged, username=username, images=images)


@app.route(basepath + 'research_forums', methods=['GET'])
def research_in_forums():
    logged = session.get("logged", False)
    username = session.get("username", None)
    data = gds.display_places(url_item, urlu, urlft, urlt, urlr, urli, urlc)
    content_research = request.args.get('content_research')
    data_filter = gds.filter(data, content_research)
    metadata = {"title":"Fiches", "pagename":"fiches"}
    return render_template('forums.html', metadata=metadata, data=data_filter, username=username, logged=logged)


@app.route(basepath + 'forum')
def forum():
    logged = session.get("logged", False)
    username = session.get("username", None)
    idForum = request.args.get('idForum', None)
    data = gds.display_instance(idForum, url_item, urlu, urlt, urlft, urlr, urlc, urli)
    metadata = {"title":"Forum", "pagename": "forum"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}
    return render_template('forum.html', data = data, metadata=metadata, logged=logged, username=username, images=images)


@app.route(basepath + 'postForum', methods=['POST'])
def com_forum():
    text_com = request.form.get("com")
    id_forum = request.form.get("id-forum")
    if request.form.get("id-com"):
        id_com = request.form.get("id-com")
    else :
        id_com = None
    newData = {
        "text": text_com,
        "user_id": session["id"],
        "text": text_com,
        "forum_id": id_forum,
        "comment_subject": id_com
    }
    metadata = {"title":"Forum", "pagename": "Forum"}
    pds.post_data('comments', data=newData)
    # on retélécharge le json pour voir le nouveau commentaire
    list_item = ['alternative_cards', 'alternative_cards_tags', 'comments', 'forums', 'forums_tags', 'impacts',
             'rooms', 'tags', 'users', 'users_alternative_cards', 'users_tags']
    dd.save_all_items(list_item)
    # ça marche pas de re afficher la page du forum ou la page forums.html --> à corriger
    data = gds.display_instance(id_forum, url_item, urlu, urlt, urlft, urlr, urlc, urli)
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}
    return render_template('forum.html', metadata=metadata, data=data, images=images)