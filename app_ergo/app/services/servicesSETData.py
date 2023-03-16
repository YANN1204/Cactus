import requests

from app.models.dataDAO import DataDAO

class SetDataServices():

    def __init__(self):
        self.pdao = DataDAO()


    def update_card(self, collection: str, new_data: dict, id: str):
        """Modifie un élément d'une 'alternative_cards' spécifique

        ***Cette fonction doit être généralisé à n'importe quelle
        collection et à n'importe quelle modification.

        Args:
            collection (str): indique la collection auquel appartient
            l'individu à modifier
            new_data (dict): dictionnaire comprenant les champs à modifier
            et le contenus
            id (str): str permettant de sélectionner l' 'alternative_cards'
            en question.
        """
        path = self.pdao.path + collection + '/' + id
        auth = ('yann.riopro@gmail.com', 'ACmerlu12')
        response = requests.patch(path,auth=auth, json=new_data)
        if response.status_code == 200:
            print('L\'enregistrement a été mis à jour avec succès')
        else:
            print(response.content)

    def update_smt(self, path: str,  id: str,new_data: dict):
        """Modifie un élément avec le path et l'id du l'item


        Args:
            collection (str): indique la collection auquel appartient
            l'individu à modifier
            new_data (dict): dictionnaire comprenant les champs à modifier
            et le contenus
            id (str): str id de l'objet en question
            place_to_add (str) : str nom du champs à ajouter
        """
        path = self.pdao.path + path + '/' + id
        auth = ('yann.riopro@gmail.com', 'ACmerlu12')
        response = requests.patch(path,auth=auth, json=new_data)
        if response.status_code == 200:
            print('L\'enregistrement a été mis à jour avec succès')
        else:
            print(response.content)

