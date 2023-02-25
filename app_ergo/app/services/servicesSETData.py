import requests
import json

from app.models.dataDAO import DataDAO

class SetDataServices():

    def __init__(self):
        self.pdao = DataDAO()
        self.base_url = self.pdao.path

    def update_card(self, card_id, new_data):
        #chemin avec l'ID de l'objet à modifier à modifier
        path = self.pdao.path + f'fiche/{card_id}'
        auth = ('yann.riopro@gmail.com', 'ACmerlu12')
        response = requests.put(path, auth=auth, json=new_data)
        if response.status_code == 200:
            print(f"L'enregistrement avec l'ID {card_id} a été modifié avec succès.")
        else:
            print(response.content)


    def set_cards(self,id_item,new_value):
        path = self.pdao.path + 'fiche'
        auth = ('yann.riopro@gmail.com', 'ACmerlu12')
        # Si je crée deux le même individu le champ room n'est pas rempli et cela crée un bug "IndexError: list index out of range"
        # lorsque je veux récupérer tout les éléments dans les services GetData
        data = {"status":"draft","title":"/new_value//","room":"c4244334-7f14-4c34-991b-a4292e7e0033"}
        response = requests.patch(path, auth=auth, json=data)
        if response.status_code == 200:
            print('L\'individu a été créé avec succès')
        else:
            print(response.content)

    import requests
import json

class SetDataServices():
    def __init__(self, base_url, project_name, api_key):
        
        
        self.api_key = api_key

    def update_data(self, collection_name, record_id, data):
        """
        Modifie un enregistrement dans Directus

        :param collection_name: nom de la collection dans Directus
        :param record_id: ID de l'enregistrement à modifier
        :param data: dictionnaire contenant les attributs à modifier

        :return: dictionnaire contenant les données mises à jour si la modification a réussi, sinon None
        """
        # Construire l'URL du endpoint pour l'enregistrement que nous souhaitons modifier
        url = f"{self.base_url}/cactus/items/{collection_name}/{record_id}"

        # Construire le corps de la requête JSON en incluant les attributs à modifier
        json_data = json.dumps(data)

        # Inclure les en-têtes HTTP requis pour la requête
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        # Envoyer la requête PATCH en utilisant la bibliothèque Python requests
        response = requests.patch(url, data=json_data, headers=headers)

        # Traiter la réponse renvoyée par l'API Directus
        if response.status_code == 200:
            updated_data = response.json()
            return updated_data
        else:
            print(f"Erreur lors de la mise à jour de l'enregistrement {record_id} : {response.text}")
            return None
