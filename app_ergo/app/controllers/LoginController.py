from flask import render_template, redirect, url_for, request, session, flash
from functools import wraps

from app import app
from app.models.dataDAO import DataDAO

dd = DataDAO()

def reqlogged(f):
      @wraps(f)
      # fonction pour vérifier la connexion avant d'accéder à une page
      def wrap(*args, **kwargs):
            
            if 'logged' in session:
                return f(*args, **kwargs)
            else:
                flash('Denied. You need to login.')
                return redirect(url_for('login'))
      return wrap


@app.route('/login', methods = ['GET', 'POST'])
def login():

    msg_error = None   

    # import des données utilisateurs 
    data = dd.get_data('users')

    # etape de connexion si l'utilisateur appuie sur le bouton 'Se connecter'
    if request.method == 'POST':
        for i in data:
            # Si le mail et le mot de passe corresponde à à ceux d'un utilisateur => déclenchement de la connexion
            if request.form['username'] == i['mail'] and request.form['password'] == i['password']:
                session['logged'] = True
                session['username'] = request.form['username']
                session['userId'] = i["id"]
                session['pseudo'] = i['pseudo']
                session['avatar'] = "https://d10b6z4v.directus.app/assets/" + i['avatar']
                # Si l'utilisateur veut adopter une pratique mais n'était pas encore connecté,
                # On le redirige après la connexion sur la fiche qu'il veut adopter directement
                if request.form.get('provide')=="True":
                    return redirect(request.referrer)
                else :
                    return redirect(url_for('accueil_connected'))              
        else: 
            msg_error = "identifiants incorrects"

    # données statique de la page
    metadata = {"title":"Login", "pagename": "login"}
    images = {'logo-cactus':url_for('static', filename="/Images/logo-cactus.png")}

    return render_template('login.html', metadata=metadata, msg_error=msg_error, provide=False, images=images)


@app.route('/logout')
@reqlogged
def logout():

    # requête données de connexion et utilisateur
    session["logged"] = False
    session["username"] = None

    # réinitialisation des données de connexion et session d'utilisateur
    session.clear()
    flash('Successfully logged out')

    return redirect(url_for('login'))
