import requests
import json

from app.models.dataDAO import DataDAO

class PostDataServices():

    def __init__(self):
        self.pdao = DataDAO()

    def post_cards(self):
        path = self.pdao.path + 'fiche'
        auth = ('yann.riopro@gmail.com', 'ACmerlu12')
        data = {"status":"draft","title":"Test","room":"c4244334-7f14-4c34-991b-a4292e7e0033"}
        response = requests.post(path, auth=auth, json=data)
        if response.status_code == 200:
            print('L\'individu a été créé avec succès')
        else:
            print(response.content)