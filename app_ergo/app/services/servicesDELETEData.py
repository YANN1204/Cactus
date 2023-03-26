import requests

from app.models.dataDAO import DataDAO

class DeleteDataServices():

    def __init__(self):
        self.pdao = DataDAO()

    def delete_cards(self, collection: str, id: int):
        """Prend une 'alternative_card' par son 'id' et envoie une requête
        à Directus pour la supprimer entièrement.

        Args:
            collection (str): la collection pour laquelle on veut
            ajouter un individu
            id (int): id pour supprimer l' 'alternative_card'

        Returns:
            message: Si la 'card' à été supprimer le message retourné indique que l'opération à
            réussi, si la requête à échoué, la fonction retourne le message d'erreur.
        """
        path = self.pdao.path + collection + '/' + id 
        response = requests.delete(path)
        if response.status_code == 200:
            return 'L\'élément a été supprimé avec succès.'
        else:
            return response.content
    
    def unadopt_card(self, index : str):
        """Supprime l'index id de la table "users_alternative_cards"

        Args:
            index (str): id de l'element a supprimer dans la table "users_alternative_cards"

        Returns:
            
        """
        path = self.pdao.path + "users_alternative_cards" + '/' + index
        response = requests.delete(path)
        if response.status_code == 200:
            return 'L\'élément a été supprimé avec succès.'
        else:
            return response.content

