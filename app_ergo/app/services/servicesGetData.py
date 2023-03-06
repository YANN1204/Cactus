import requests
import json

from app.models.dataDAO import DataDAO

class GetDataServices():

    def __init__(self):
        self.pdao = DataDAO()

    def display_data(self, url):
        data = self.pdao.get_data(url)
        return data

    def display_title(self, url):
        data = self.pdao.get_data(url)['data']
        title = []
        for i in data:
            title.append(i['title'])

    def room_by_alternative(self, url):
        id_room = {'032160c4-caa2-451f-b3c8-72c53360345f': 'Salle de bain', '8a855849-86a0-47e0-b4ff-c240f6e6bf4f': 'Cuisine'}
        data = self.pdao.get_data(url)['data']
        room = {}
        for i in data:
            room[i['title']] = id_room[str(i['room_id'])]
        list_room = []
        for i in room:
            list_room.append((i, room.get(i)))
        return list_room

    def alternative_by_title(self, url, title):
        data = self.pdao.get_data(url)['data']
        for i in data:
            if i['title'] == title:
                return i
        return 'Aucun élément ne présente ce titre dans la base de donnée'
