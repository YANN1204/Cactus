from flask import render_template
from app import app

from app.services.servicesGETData import GetDataServices

gds = GetDataServices()

basepath = '/'
url = "forums"

@app.route(basepath + 'forums', methods = ['GET'])
def forums():
    data = gds.display_data(url)
    metadata = {"title":"Forums", "pagename": "forums"}
    return render_template('forums.html', data=data, metadata=metadata)