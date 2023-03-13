import requests
import json

from app.models.dataDAO import DataDAO



class PostDataServices():


    def __init__(self):
        self.pdao = DataDAO()


    def post_data(self, collection: str, data: dict):
        """Crée un individu pour une collection donnée avec un status
        un titre et une pièce de la maison sur Directus.
        ***Cette fonction est amené à être généralisé.
        Args:
            collection (str): la collection dans laquelle on veut 
            ajouter un élément
            data (dict): un dictionnaire avec tout les champs renseigné et
            le contenu associé
        """
        path = self.pdao.path + collection
        auth = ('yann.riopro@gmail.com', 'ACmerlu12')
        response = requests.post(path, auth=auth, json=data)
        if response.status_code == 200:
            print('L\'individu a été créé avec succès')
        else:
            print(response.content)