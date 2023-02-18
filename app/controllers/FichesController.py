from flask import render_template, redirect, url_for
from app import app
from app.services.servicesPostData import PostDataServices

sds = PostDataServices()

basepath = '/'
data = sds.post_cards()

@app.route(basepath + 'fiches', methods = ['GET'])
def fiches():
    metadata = {"title":"Fiches", "pagename": "fiches"}
    print(data)
    return render_template('fiches.html', metadata=metadata)