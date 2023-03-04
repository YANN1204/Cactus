import requests
<<<<<<< HEAD
=======
import json
>>>>>>> 314a96df03c2a329d4915e33f13e930e2f90ed44

from app.models.dataDAO import DataDAO

class SetDataServices():

    def __init__(self):
        self.pdao = DataDAO()


    def update_card(self, id):
<<<<<<< HEAD
        #chemi avec l'ID de l'objet à modifier à modifier
        path = self.pdao.path+"fiche/"+id
        print(path)
        auth = ('yann.riopro@gmail.com', 'ACmerlu12')
=======
        #chemin avec l'ID de l'objet à modifier à modifier
        path = self.pdao.path+"fiche/"+id
        print(path)
        auth = ('dylan.canete5@etu.univ-lorraine.fr', 'dylan')
>>>>>>> 314a96df03c2a329d4915e33f13e930e2f90ed44
        new_data={"title":"Test2"}
        response = requests.patch(path,auth=auth, json=new_data)
        if response.status_code == 200:
            print('L\'enregistrement a été mis à jour avec succès')
        else:
<<<<<<< HEAD
            print(response.content)
=======
            print(response.content)
>>>>>>> 314a96df03c2a329d4915e33f13e930e2f90ed44
