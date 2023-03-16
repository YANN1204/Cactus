import signal
from flask import Flask, session
from flask_session import Session
import sys

app = Flask(__name__, static_url_path='/static')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.secret_key = 'une_cle_secrete_pour_la_session'
Session(app)

def signal_handler(signal, frame):
    # Réinitialiser la session Flask lorsque l'application est arrêtée
    session.clear()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

from app.controllers import *