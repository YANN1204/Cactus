import requests
import json

from app.models.dataDAO import DataDAO

class DeleteDataServices():

    def __init__(self):
        self.pdao = DataDAO()

    def delete_cards(self, id: int):
        """Prend une 'alternative_card' par son 'id' et envoie une requête
        à Directus pour la supprimer entièrement.

        Args:
            id (int): id pour supprimer l' 'alternative_card'

        Returns:
            message: Si la 'card' à été supprimer le message retourné indique que l'opération à
            réussi, si la requête à échoué, la fonction retourne le message d'erreur.
        """
        path = self.pdao.path + 'alternative_cards/' + id 
        response = requests.delete(path)
        if response.status_code == 200:
            return 'L\'élément a été supprimé avec succès.'
        else:
            return response.content