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
        id_room = {'c4244334-7f14-4c34-991b-a4292e7e0033': 'Salle de bain', 'b98230d9-c106-4bd1-9765-cf7e0308113c': 'Cuisine'}
        data = self.pdao.get_data(url)['data']
        room = {}
        for i in data:
            room[i['title']] = id_room[str(i['room'])]
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
