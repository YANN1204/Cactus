import signal
from flask import Flask, session
from flask_session import Session
import sys
from app.models.dataDAO import DataDAO

app = Flask(__name__, static_url_path='/static')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.secret_key = 'une_cle_secrete_pour_la_session'
Session(app)

def signal_handler(signal, frame):
    # Réinitialiser la session Flask lorsque l'application est arrêtée
    session.clear()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# import de la base de donnée
list_item = ['alternative_cards', 'alternative_cards_tags', 'comments', 'forums', 'forums_tags', 'impacts',
             'rooms', 'tags', 'users', 'users_alternative_cards', 'users_tags']
dd = DataDAO()
dd.save_all_items(list_item)

from app.controllers import *