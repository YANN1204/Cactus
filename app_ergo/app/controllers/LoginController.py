from flask import render_template, redirect, url_for, request, session, flash
from app import app
from functools import wraps
from app.models.dataDAO import DataDAO

dd = DataDAO()
urlu = "users"

def reqlogged(f):
      @wraps(f)
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
    data = dd.get_data('users')
    if request.method == 'POST':
        for i in data:
            if request.form['username'] == i['mail'] or request.form['password'] == i['password']:
                session['logged'] = True
                session['username'] = request.form['username']
                return redirect(url_for('accueil_connected'))
        else: 
            msg_error = "identifiants incorrects"

    metadata = {"title":"Login", "pagename": "login"}
    return render_template('login.html', metadata=metadata, msg_error=msg_error)


@app.route('/logout')
@reqlogged
def logout():
    session["logged"] = False
    session["username"] = None
    session.clear()
    flash('Successfully logged out')
    return redirect(url_for('login'))