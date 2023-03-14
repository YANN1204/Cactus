from flask import render_template, redirect, request, url_for
import requests
import os
from app import app
from app.services.servicesPOSTData import PostDataServices

pds = PostDataServices()

basepath = '/'

@app.route(basepath + 'sign_up', methods = ['GET'])
def sign_up():
    metadata = {"title":"Sign_up", "pagename": "sign_up"}
    return render_template('sign_up.html', metadata=metadata)


@app.route(basepath + 'register', methods=['POST'])
def register():
    # Récupérer les valeurs de l'e-mail, du mot de passe et de l'adresse e-mail depuis le formulaire
    email = request.form.get("email")
    password = request.form.get("password")        
    avatar= request.form.get("avatar")
    pseudo=request.form.get("pseudo")    
    avatar = request.files.get("avatar")

        # Enregistrer l'avatar dans le dossier statique
    filename = avatar.filename
    filepath = os.path.join('statique', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    avatar.save(filepath)
    # Créer un nouvel utilisateur dans Directus avec ces valeurs
    newData = {
        "mail": email,
        "password": password,
        "pseudo": pseudo,
        "avatar": filepath
    }
    metadata = {"title": "Sign_up", "pagename": "sign_up"}


    data = pds.post_data('users', data=newData)
    return render_template('sign_up.html', metadata=metadata, data=data)