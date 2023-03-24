from flask import render_template, session, request
import requests
import os
from app import app
from app.services.servicesPOSTData import PostDataServices
from app.services.servicesGETData import GetDataServices
from app.services.servicesSETData import SetDataServices
from app.models.dataDAO import DataDAO
from PIL import Image

pds = PostDataServices()
gds = GetDataServices()
sds = SetDataServices()
dd = DataDAO()
app.config['UPLOAD_FOLDER'] = 'app_ergo/app/static'
urlt = "tags"

basepath = '/'


@app.route(basepath + 'sign_up', methods = ['GET'])
def sign_up():
    data=dd.get_data(url=urlt)
    
    metadata = {"title":"Sign_up", "pagename": "sign_up"}
    return render_template('sign_up.html',data=data, metadata=metadata)


@app.route(basepath + 'register', methods=['POST'])
def register():
    # Récupérer les valeurs de l'e-mail, du mot de passe et de l'adresse e-mail depuis le formulaire
    email = request.form.get("email")
    password = request.form.get("password")  
    id_avatar=0
    #tag = request.form.get("result")      
    #avatar= request.form.get("avatar")
    pseudo=request.form.get("pseudo")   
    avatar_number = request.form.get('image')    
    #selection de l'avatar
    if avatar_number=="1.png":
        id_avatar="c9f1537e-5047-4d28-b2ea-75b8a1cd1fd7"
    if avatar_number=="2.png":
        id_avatar="bfbee79a-e1f2-48f3-865e-71c53c2a6650"
    if avatar_number=="3.png":
        id_avatar="04bbc5e6-d05d-4376-bbd1-1e5d0afae53e"
    if avatar_number=="4.png":
        id_avatar="e6dad96c-4d70-43ba-98b4-4ae5d6dec8b6"
    # Créer un nouvel utilisateur dans Directus avec ces valeurs
    newData = {
        "mail": email,
        "password": password,
        "pseudo": pseudo,
        #"tagId": tag        
        "avatar": id_avatar
    }
    metadata = {"title": "Sign_up", "pagename": "sign_up"}

    data = pds.post_data('users', data=newData)  

    # import de la base de donnée
    list_item = ['alternative_cards', 'alternative_cards_tags', 'comments', 'forums', 'forums_tags', 'impacts','rooms', 'tags', 'users', 'users_alternative_cards', 'users_tags']
    dd = DataDAO()
    dd.save_all_items(list_item)
    return render_template('login.html', metadata=metadata, data=data)

