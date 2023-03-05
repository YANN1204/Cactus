import requests

from app.models.dataDAO import DataDAO

class SetDataServices():

    def __init__(self):
        self.pdao = DataDAO()


    def update_card(self, id):
        #chemi avec l'ID de l'objet à modifier à modifier
        path = self.pdao.path+"alternative_cards/"+id
        print(path)
        auth = ('yann.riopro@gmail.com', 'ACmerlu12')
        new_data={"title":"Test2"}
        response = requests.patch(path,auth=auth, json=new_data)
        if response.status_code == 200:
            print('L\'enregistrement a été mis à jour avec succès')
        else:
            print(response.content)