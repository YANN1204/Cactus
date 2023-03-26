from flask import render_template, request, url_for
import json

from app import app
from app.services.servicesPOSTData import PostDataServices
from app.services.servicesGETData import GetDataServices
from app.services.servicesSETData import SetDataServices
from app.models.dataDAO import DataDAO


pds = PostDataServices()
gds = GetDataServices()
sds = SetDataServices()
dd = DataDAO()

app.config['UPLOAD_FOLDER'] = 'app_ergo/app/static'

file_path = "app\static\items_directus.json"
with open(file_path, 'r') as f:
    items_directus = json.load(f)

basepath = '/'


@app.route(basepath + 'sign_up', methods = ['GET'])
def sign_up():

    # requête des différents tags de la base de données
    data=dd.get_data(url=items_directus['urlt'])
    
    # données statique de la page
    metadata = {"title":"Sign_up", "pagename": "sign_up"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}

    return render_template('sign_up.html',data=data, metadata=metadata, images=images)


@app.route(basepath + 'register', methods=['POST'])
def register():

    # requête données de connexion et utilisateur
    email = request.form.get("email")
    password = request.form.get("password")  
    id_avatar=0
    pseudo=request.form.get("pseudo")   
    avatar_number = request.form.get('image')  

    #selection de l'avatar
    if avatar_number=="1.png":
        id_avatar="c9f1537e-5047-4d28-b2ea-75b8a1cd1fd7"
    if avatar_number=="2.png":
        id_avatar="bfbee79a-e1f2-48f3-865e-71c53c2a6650"
    if avatar_number=="3.png":
        id_avatar="75b54802-d999-43d9-9468-d791126d5cd9"
    if avatar_number=="4.png":
        id_avatar="e6dad96c-4d70-43ba-98b4-4ae5d6dec8b6"

    # Créer un nouvel utilisateur dans Directus avec ces valeurs
    newData = {
        "mail": email,
        "password": password,
        "pseudo": pseudo,       
        "avatar": id_avatar
    }
    
    # Enregistrement du nouvel utilisateur inscrit dans la base de donnée
    data = pds.post_data('users', data=newData)  

    # mise à jour de la base de donnée
    list_item = list(items_directus.values()) 
    dd.save_all_items(list_item)

    # données statique de la page
    metadata = {"title": "Sign_up", "pagename": "sign_up"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}

    return render_template('login.html', metadata=metadata, data=data, images=images)

