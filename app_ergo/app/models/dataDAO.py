import requests
import json 
import os



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

        file_path = "app\static\database\database.json"
        with open(file_path, 'r') as f:
            all_data = json.load(f)
        data = all_data[url]

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


    def save_all_items(self, list_items):
        """Permet de créer un fichier json dans le chemin
        "app/static/database/database.json" contenant toutes
        les données de l'api Directus

        Args:
            list_items (list): liste contenants tout les
            noms des items de la base de donnée Directus

        Returns:
            dict: dictionnaire de toute les données de l'API
            Directus
        """
        all_items = {}
        for i in list_items:
            response = requests.get(self.path + i)
            data = json.loads(response.text)
            all_items[i] = data['data']
    
        try:
            with open('app/static/database/database.json', 'w') as f:
                json.dump(all_items, f)
        except IOError:
            print("Erreur: impossible de créer ou d'écrire dans le fichier 'database.json'")

        return all_items
            