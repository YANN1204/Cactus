import requests

from app.models.dataDAO import DataDAO

class SetDataServices():

    def __init__(self):
        self.pdao = DataDAO()


    def update_card(self, id: str):
        """Modifie un élément d'une 'alternative_cards' spécifique

        ***Cette fonction doit être généralisé à n'importe quelle
        collection et à n'importe quelle modification.

        Args:
            id (str): str permettant de sélectionner l' 'alternative_cards'
            en question.
        """
        path = self.pdao.path+"alternative_cards/"+id
        print(path)
        auth = ('yann.riopro@gmail.com', 'ACmerlu12')
        new_data={"title":"Test2"}
        response = requests.patch(path,auth=auth, json=new_data)
        if response.status_code == 200:
            print('L\'enregistrement a été mis à jour avec succès')
        else:
            print(response.content)