import requests
import json

from app.models.dataDAO import DataDAO

class DeleteDataServices():

    def __init__(self):
        self.pdao = DataDAO()

    def delete_cards(self, id):
        path = self.pdao.path + 'fiche/' + id 
        auth = ('yann.riopro@gmail.com', 'ACmerlu12')
        response = requests.delete(path)
        if response.status_code == 200:
            return 'L\'élément a été supprimé avec succès.'
        else:
            return response.content