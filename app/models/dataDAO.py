import requests
import json 

class DataDAO():

    def __init__(self):
        self.path = "https://d10b6z4v.directus.app/items/"

    def get_data(self, url):

        response = requests.get(self.path + url)
        data = json.loads(response.text)

        return data