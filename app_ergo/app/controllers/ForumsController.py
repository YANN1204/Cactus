from flask import render_template, redirect, url_for
from app import app

from app.services.servicesGetData import GetDataServices

gds = GetDataServices()

basepath = '/'
url = "fiche"

@app.route(basepath + 'forums', methods = ['GET'])
def forums():
    data = gds.alternative_by_title(url, "Test")
    metadata = {"title":"Forums", "pagename": "forums"}
    return render_template('forums.html', data=data, metadata=metadata)