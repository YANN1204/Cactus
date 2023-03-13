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
urlc = "comments"


@app.route(basepath + 'forums', methods = ['GET'])
def forums():
    data = gds.display_forums_fiches(urlf, urlu, urlft, urlt, urlr)
    metadata = {"title":"Forums", "pagename": "forums"}
    return render_template('forums.html', data=data, metadata=metadata)


@app.route('/forum')
def forum():
    idForum = request.args.get('idForum', None)
    data = gds.display_forum(idForum, urlf, urlu, urlt, urlft, urlr, urlc)
    metadata = {"title":"Forum", "pagename": "forum"}
    return render_template('forum.html', data = data, metadata=metadata)