from flask import render_template, session, request
import requests
import os
from app import app
from app.services.servicesPOSTData import PostDataServices
from app.services.servicesGETData import GetDataServices
from app.models.dataDAO import DataDAO

pds = PostDataServices()
gds = GetDataServices()
dd = DataDAO()

urlt = "tags"

basepath = '/'


@app.route(basepath + 'sign_up', methods = ['GET'])
def sign_up():
    is_connected = session.get("is_connected", False)
    data=dd.get_data(url=urlt)
    
    metadata = {"title":"Sign_up", "pagename": "sign_up"}
    return render_template('sign_up.html',data=data, metadata=metadata)


@app.route(basepath + 'register', methods=['POST'])
def register():
    # Récupérer les valeurs de l'e-mail, du mot de passe et de l'adresse e-mail depuis le formulaire
    email = request.form.get("email")
    password = request.form.get("password")  
    print(email)
    #tag = request.form.get("result")      
    #avatar= request.form.get("avatar")
    pseudo=request.form.get("pseudo")    
    #avatar = request.files.get("avatar")

        # Enregistrer l'avatar dans le dossier statique
    #filename = avatar.filename
    #filepath = os.path.join('statique', filename)
    #os.makedirs(os.path.dirname(filepath), exist_ok=True)
    #avatar.save(filepath)
    # Créer un nouvel utilisateur dans Directus avec ces valeurs
    newData = {
        "mail": email,
        "password": password,
        "pseudo": pseudo,
        #"tagId": tag
        #"avatar": filepath
    }
    metadata = {"title": "Sign_up", "pagename": "sign_up"}


    data = pds.post_data('users', data=newData)
    return render_template('login.html', metadata=metadata, data=data)

