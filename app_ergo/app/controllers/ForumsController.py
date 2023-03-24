from flask import Flask, render_template, request, session
from app import app

from app.services.servicesGETData import GetDataServices

gds = GetDataServices()


basepath = '/'
# les noms des différentes collection associées à l'item qui nous
# intéresse ici (forum)
url_item = "forums"
urlu = "users"
urlt = "tags"
urlft = "forums_tags"
urlr = "rooms"
urlc = "comments"


@app.route(basepath + 'forums', methods = ['GET'])
def forums():
    logged = session.get("logged", False)
    username = session.get("username", None)
    data = gds.display_places(url_item, urlu, urlft, urlt, urlr)
    metadata = {"title":"Forums", "pagename": "forums"}
    return render_template('forums.html', data=data, metadata=metadata, logged=logged, username=username)

@app.route(basepath + 'research_forums', methods=['GET'])
def research_in_forums():
    logged = session.get("logged", False)
    username = session.get("username", None)
    data = gds.display_places(url_item, urlu, urlft, urlt, urlr)
    content_research = request.args.get('content_research')
    data_filter = gds.filter(data, content_research)
    metadata = {"title":"Fiches", "pagename":"fiches"}
    return render_template('forums.html', metadata=metadata, data=data_filter, username=username, logged=logged)


@app.route('/forum')
def forum():
    logged = session.get("logged", False)
    username = session.get("username", None)
    idForum = request.args.get('idForum', None)
    data = gds.display_instance(idForum, url_item, urlu, urlt, urlft, urlr, urlc)
    metadata = {"title":"Forum", "pagename": "forum"}
    return render_template('forum.html', data = data, metadata=metadata, logged=logged, username=username)