from flask import render_template
from app import app

from app.services.servicesGETData import GetDataServices

gds = GetDataServices()

basepath = '/'
url = "alternative_cards"

@app.route(basepath + 'forums', methods = ['GET'])
def forums():
    data = gds.alternative_by_title(url, "Boire l'eau du robinet grâce à une carafe filtrante")
    metadata = {"title":"Forums", "pagename": "forums"}
    return render_template('forums.html', data=data, metadata=metadata)
