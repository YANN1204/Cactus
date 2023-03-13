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
    
    def get_instance(self, url: str, id: str):
        """Retourne les informations sous la forme d'un
        dictionnaire d'une seul instance d'un item (ou collection)
        sur Directus avec son id

        Args:
            url (str): de la collection où item où l'on veut
            récupérer l'instance
            id (str): l'id de l'instance dont l'on veut récupérer
            les informations

        Returns:
            dict: les données sur l'instance que l'on veut récupérer
        """
        response = requests.get(self.path + url + '/' + id)
        data = json.loads(response.text)

        return data