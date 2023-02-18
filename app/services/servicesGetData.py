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
        id_room = {'1': 'Salle de bain', '3': 'Cuisine'}
        data = self.pdao.get_data(url)['data']
        room = {}
        for i in data:
            room[i['title']] = id_room[str(i['room'][0])]
        list_room = []
        for i in room:
            list_room.append((i, room.get(i)))
        return list_room
