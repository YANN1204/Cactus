import requests
import json

from app.models.dataDAO import DataDAO



class PostDataServices():


    def __init__(self):
        self.pdao = DataDAO()


    def post_cards(self):

        path = self.pdao.path + 'alternative_cards'
        auth = ('yann.riopro@gmail.com', 'ACmerlu12')
        data = {"status":"draft","title":"Test","room_id":"032160c4-caa2-451f-b3c8-72c53360345f"}
        response = requests.post(path, auth=auth, json=data)
        if response.status_code == 200:
            print('L\'individu a été créé avec succès')
        else:
            print(response.content)