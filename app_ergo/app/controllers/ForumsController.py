from flask import Flask, render_template, request
from app import app

from app.services.servicesGETData import GetDataServices

gds = GetDataServices()

basepath = '/'
urlf = "forums"
urlu = "users"
urlt = "tags"
urlft = "forums_tags"
urlr = "rooms"


@app.route(basepath + 'forums', methods = ['GET'])
def forums():
    data = gds.display_forums_fiches(urlf, urlu, urlft, urlt, urlr)
    metadata = {"title":"Forums", "pagename": "forums"}
    return render_template('forums.html', data=data, metadata=metadata)


@app.route('/forum')
def forum():
    idForum = request.args.get('idForum', None)
    data = gds.item_by_id(urlf, idForum)
    metadata = {"title":"Forum", "pagename": "forum"}
    return render_template('forum.html', data = data, metadata=metadata)