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

@app.route(basepath + 'communaute', methods = ['GET'])
def communaute():
    logged = session.get("logged", False)
    username = session.get("username", None)
    data = {}
    data['tot_impacts'] = gds.impact_total_sum(items_directus['urli'])
    data['impact_per_month'] = gds.impact_per_month(items_directus['urli'])

    metadata = {"title":"Impact communaute", "pagename": "Impact communaute"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}
    return render_template('communaute.html', metadata=metadata, data=data, logged=logged, username=username, images=images)

@app.route('/plot_plastique_com.png')
def plot_plastique_com():
    fig1 = gds.graph(items_directus['urli'], 'plastique')
    output = io.BytesIO()
    FigureCanvas(fig1).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plot_co2_com.png')
def plot_co2_com():
    fig2 = gds.graph(items_directus['urli'], 'co2')
    output = io.BytesIO()
    FigureCanvas(fig2).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plot_eau_com.png')
def plot_eau_com():
    fig3 = gds.graph(items_directus['urli'], 'eau')
    output = io.BytesIO()
    FigureCanvas(fig3).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')