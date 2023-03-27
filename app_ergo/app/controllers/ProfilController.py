from flask import render_template, session, url_for, Response
import json

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

from app import app
from app.controllers.LoginController import reqlogged
from app.services.servicesGETData import GetDataServices

file_path = "app\static\items_directus.json"
with open(file_path, 'r') as f:
    items_directus = json.load(f)

gds = GetDataServices()

basepath = '/'

@app.route(basepath + 'profil', methods = ['GET'])
@reqlogged
def profil():

    # requête données de connexion et utilisateur
    logged = session.get("logged", False)
    username = session.get("username", None)

    # requêtes des données d'impacts personnalisés de l'utilisateur
    data = {}
    data['cards_adopted'] = gds.cards_adopted(session['userId'])
    data['cards_suggested'] = gds.cards_suggested(session['userId'])
    data['tot_impacts'] = gds.impact_total_sum(items_directus['urli'], id = session['userId'])
    data['impact_per_month'] = gds.impact_per_month(items_directus['urli'], id = session['userId'])

    # données statique de la page
    metadata = {"title":"Profil", "pagename": "profil"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}
    return render_template('profil.html', metadata=metadata, data=data, logged=logged, username=username, images=images)


@app.route('/plot_plastique.png')
def plot_plastique():
    # graphe pour le topic plastique
    fig1 = gds.graph(items_directus['urli'], 'plastique', id=session['userId'])
    output = io.BytesIO()
    FigureCanvas(fig1).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/plot_co2.png')
def plot_co2():
    # graphe pour le topic co2
    fig2 = gds.graph(items_directus['urli'], 'co2', id=session['userId'])
    output = io.BytesIO()
    FigureCanvas(fig2).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/plot_eau.png')
def plot_eau():
    # graphe pour le topic eau
    fig3 = gds.graph(items_directus['urli'], 'eau', id=session['userId'])
    output = io.BytesIO()
    FigureCanvas(fig3).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
