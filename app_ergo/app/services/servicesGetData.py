import requests
import json

from app.models.dataDAO import DataDAO



class GetDataServices():


    def __init__(self):
        self.pdao = DataDAO()


    def display_data(self, url: str):
        """Affiche les données sous la forme d'un dictionnaire python

        Args:
            url (str): url servant à afficher les données
            que l'on veut afficher

        Returns:
            dict: les données sous forme de dictionnaire 
        """
        data = self.pdao.get_data(url)
        return data


    def display_title(self, url: str):
        """Retourne tout les titre des éléments
        d'une collection particulière de Directus 

        Args:
            url (str): url de la collection recherché

        Returns:
            list: la liste des titres
        """
        data = self.pdao.get_data(url)['data']
        title = []
        for i in data:
            title.append(i['title'])
        return title


    def room_by_alternative(self, url: str):
        """Retourne un dictionnaire avec en clé
        le titre de l'alternative_cards et en valeur le
        nom de la pièce de la maison qui lui est associé.
        
        ***Cette fonction sera amené à être généralisé

        Args:
            url (str): url de la collection (alternative_cards
            dans cette exemple)

        Returns:
            dict: retourne le dictionnaire avec les élements titre & pièces
            de la maison associé
        """
        id_room = {'032160c4-caa2-451f-b3c8-72c53360345f': 'Salle de bain', '8a855849-86a0-47e0-b4ff-c240f6e6bf4f': 'Cuisine'}
        data = self.pdao.get_data(url)['data']
        room = {}
        for i in data:
            room[i['title']] = id_room[str(i['room_id'])]
        list_room = []
        for i in room:
            list_room.append((i, room.get(i)))
        return list_room


    def alternative_by_title(self, url: str, title: str):
        """Retourne l'ensemble des informations d'une
        collection données à partir de son titre

        Args:
            url (str): nom de la collection recherché
            title (str): titre de l'élément dont l'on veut
            récupérer les informations

        Returns:
            dict: un dictionnaire avec toutes les informations de
            l'élément de la collection, si le titre n'a pas été
            trouvé, la fonction renvoie un message d'erreur.
        """
        data = self.pdao.get_data(url)['data']
        for i in data:
            if i['title'] == title:
                return i
        return 'Aucun élément ne présente ce titre dans la base de donnée'
