import requests
import json

from app.models.dataDAO import DataDAO

class PostDataServices():

    def __init__(self):
        self.pdao = DataDAO()

    def post_cards(self):
        path = self.pdao.path + 'fiche'
        auth = ('yann.riopro@gmail.com', 'ACmerlu12')
        data = {"status":"draft","title":"J'ai réussi à crée une alternative depuis le client web","room":[3]}
        response = requests.post(path, auth=auth, json=data)
        if response.status_code == 200:
            return 'L\'individu a été créé avec succès'
        else:
            return response.content