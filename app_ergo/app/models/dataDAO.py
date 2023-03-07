import requests
import json 



class DataDAO():


    def __init__(self):
        self.path = "https://d10b6z4v.directus.app/items/"


    def get_data(self, url: str):
        """Retourne les informations sous la forme d'un 
        fichier dictionnaire à partir d'une requête GET 
        envoyé à Directus qui retourne un fichier json

        Args:
            url (str): url de la collection dont l'on
            veut récupérer les données

        Returns:
            dict: données de la collection sous forme
            de dictionnaire
        """
        response = requests.get(self.path + url)
        data = json.loads(response.text)

        return data