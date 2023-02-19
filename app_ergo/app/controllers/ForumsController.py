from flask import render_template, redirect, url_for
from app import app

basepath = '/'

@app.route(basepath + 'forums', methods = ['GET'])
def forums():
    metadata = {"title":"Forums", "pagename": "forums"}
    return render_template('forums.html', metadata=metadata)