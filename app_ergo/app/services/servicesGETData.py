from app.models.dataDAO import DataDAO
import datetime
from datetime import datetime



class GetDataServices():


    def __init__(self):
        self.pdao = DataDAO()


    def display_data(self, url: str):
        """Affiche les données sous la forme d'un dictionnaire python

        Args:
            url (str): url servant à afficher les données
            que l'on veut afficher

        Returns:
            dict: les données sous forme d'un dictionnaire qui contient une liste de dictionnaires,
                un dictionnaire par item
        """
        data = self.pdao.get_data(url)
        return data
    ##remplacer get data par get instance pour modifier les alternative adopté


    def display_places(self, url_item: str, urlu: str, urlft: str, urlt: str, urlr: str):
        """Affiche les données sous la forme d'un dictionnaire python
           # impact à rajouter
           # doit certainement pouvoir être optimisé car chargement assez long... 
           # + ajouter vérif éventuellement

        Args:
            url (str): url servant à afficher les forums ou fiches
            urlu (str) : url servant à faire la correspondance entre user_id et pseudo de l'user
            urlft (str) : url servant à faire la correspondance entre id du tag et forum/fiche et id du tag
            urlt (str) : url servant à faire la correspondance entre tag_id et tag_name
            urlr (str) : url servant à faire la correspondance entre room_id et room_name

        Returns:
            dict: les données sous forme de dictionnaire avec des entrées supplémentaires permettant
            de récupérer les noms à la place des id du modèle de données
        """
        data = self.pdao.get_data(url_item)

        # parcourt la liste d'items du dictionnaire data
        for item in data :
            #print(item)
            item['date_created'] = self.convert_date(item['date_created'])
            # récupère les infos du user avec l'id correspondant au champ user_id du forum/fiche
            user = self.instance_by_id(urlu, item['user_id'])
            # crée une nouvelle key pseudo au dict du forum/fiche avec comme valeur le pseudo correspondant à l'user
            item['pseudo'] = user['pseudo']
            # on récupère la liste de noms de tags
            tags_name = self.find_tag(urlft, urlt, item["tag"])
            # on ajoute la liste de noms de tags à une nouvelle entrée du dict forum/fiche
            item['tags_name'] = tags_name
            # même chose pour avoir le room_name
            room = self.instance_by_id(urlr, item['room_id'])
            item['room_name'] = room['room_name']

        return data
    

    def find_tag(self, urlft: str, urlt: str, list_tag: list):
        """Affiche les données sous la forme d'une liste

        Args:
            urlft (str) : url servant à faire la correspondance entre id du tag et forum/fiche et id du tag
            urlt (str) : url servant à faire la correspondance entre tag_id et tag_name
            list_tag (list) : liste d'id de relation tags-forums ou tags-fiches

        Returns:
            list : liste des tag_name pour un forum/fiche
        """
        # parcourt la liste d'id contenu dans le champ tag du forum/fiche
        # ces id correspondent aux id des croisements de forum/fiche et tags (table forums_tags/ alternative_cards_tags)
        tags_name = []
        for t in list_tag:
            # récupère l'id du tag du lien tag-forum / tag-fiche
            tag_id = self.instance_by_id(urlft, t)
  
            # récupère le nom du tag avec l'id récupéré avant
            tag = self.instance_by_id(urlt, tag_id["tags_id"])
            
            tags_name.append(tag['tag_name'])
            
        return tags_name


    def convert_date(self, date: str) :
        """Convertit la date au format jj/mm/aaaa

        Args:
            date (str) : la date à convertir

        Returns:
            date : string de la date convertie
        """
        timestamp = date[0:19]
        timestamp = datetime.strptime((timestamp), "%Y-%m-%dT%H:%M:%S")
        date = timestamp.strftime("%d/%m/%Y")
        return date


    def display_instance(self, idInstance: str, url_item: str, urlu: str, urlt: str, urlft: str, urlr: str, urlc: str):
        # pas fini
        data = self.instance_by_id(url_item, idInstance)
        data['date_created'] = self.convert_date(data['date_created'])
        # récupère les infos du user avec l'id correspondant au champ user_id du forum/fiche
        user = self.instance_by_id(urlu, data['user_id'])
        # crée une nouvelle key pseudo au dict du forum/fiche avec comme valeur le pseudo correspondant à l'user
        data['pseudo'] = user['pseudo']
        data['avatar'] = "https://d10b6z4v.directus.app/assets/" + user['avatar']
        # on récupère la liste de noms de tags
        tags_name = self.find_tag(urlft, urlt, data["tag"])
        # on ajoute la liste de noms de tags à une nouvelle entrée du dict forum/fiche
        data['tags_name'] = tags_name
        # même chose pour avoir le room_name
        room = self.instance_by_id(urlr, data['room_id'])
        data['room_name'] = room['room_name']
        data['comments'] = self.find_comments(idInstance, urlc, urlu)
        return data

    def find_comments(self, idInstance: str, urlc: str, urlu: str):
        """Retourne tous les commentaires d'une fiche ou d'un forum 

        Args:
            urlc (str): url de la collection comments
            urlu (str): url de la collection users

        Returns:
            comments: la liste des commentaires avec pseudo et avatr des users qui l'ont posté
        """
        data = self.pdao.get_data(urlc)
        comments = []
        for c in data:
            if c['forum_id'] == idInstance:
                comments.append(c)
                user = self.instance_by_id(urlu, c['user_id'])
                c['pseudo'] = user['pseudo']
                c['avatar'] = "https://d10b6z4v.directus.app/assets/" + user['avatar']
                c['date_created'] = self.convert_date(c['date_created'])
            elif  c['alternative_card_id'] == idInstance:
                comments.append(c)
                user = self.instance_by_id(urlu, c['user_id'])
                c['pseudo'] = user['pseudo']
                c['avatar'] = "https://d10b6z4v.directus.app/assets/" + user['avatar']
                c['date_created'] = self.convert_date(c['date_created'])
                if c['comment_type'] == "1" :
                    c['comment_type'] = "Commentaire"
                elif c['comment_type'] == "2" :
                    c['comment_type'] = "Suggestion"
        return comments


    def display_title(self, url: str):
        """Retourne tout les titre des éléments
        d'une collection particulière de Directus 

        Args:
            url (str): url de la collection recherché

        Returns:
            list: la liste des titres
        """
        data = self.pdao.get_data(url)
        title = []
        for i in data:
            title.append(i['title'])
        return title


    def room_by_alternative(self, url: str):
        """Retourne un dictionnaire avec en clé
        le titre de l'alternative_cards et en valeur le
        nom de la pièce de la maison qui lui est associé.
        
        ***Cette fonction sera amené à être généralisé

        Args:
            url (str): url de la collection (alternative_cards
            dans cette exemple)

        Returns:
            dict: retourne le dictionnaire avec les élements titre & pièces
            de la maison associé
        """
        id_room = {'032160c4-caa2-451f-b3c8-72c53360345f': 'Salle de bain', '8a855849-86a0-47e0-b4ff-c240f6e6bf4f': 'Cuisine'}
        data = self.pdao.get_data(url)
        room = {}
        for i in data:
            room[i['title']] = id_room[str(i['room_id'])]
        list_room = []
        for i in room:
            list_room.append((i, room.get(i)))
        return list_room


    def item_by_title(self, url: str, title: str):
        """Retourne l'ensemble des informations d'une
        collection données à partir de son titre

            récupérer les informations
        Returns:
            dict: un dictionnaire avec toutes les informations de
            l'élément de la collection, si le titre n'a pas été
            trouvé, la fonction renvoie un message d'erreur.
        """
        data = self.pdao.get_data(url)
        for i in data:
            if i['title'] == title:
                return i
        return 'Aucun élément ne présente ce titre dans la base de donnée'
    

    def instance_by_id(self, url: str, id: str):
        """Retourne l'ensemble des informations d'une
        instance d'une collection données à partir de 
        son id

        Args:
            url (str): nom de la collection recherché
            id (str): id de l'élément dont l'on veut
            récupérer les informations

        Returns:
            dict: un dictionnaire avec toutes les informations de
            l'élément de la collection, si l'id n'a pas été
            trouvé, la fonction renvoie un message d'erreur.
        """
        data = self.pdao.get_data(url)
        
        for i in data:
            if i['id'] == id:
                return i
            
        return 'Aucun élément ne présente cet id dans la base de donnée'
    

    def instance_by_attribute(self, url: str, attribute: str, content_attribute: str):
        """Cette fonction est une généralisation de la fonction instance_by_id et permet
        de récupérer l'instance d'une collection à partir de n'importe lequel de ces
        champs ou attribut

        Args:
            url (str): _description_
            attribute (str): l'attribut qui servira à la reconnaissance
            de l'instance (celle-ci ne doit pas contenir des instances qui ont
            la même valeur pour cet attribut)
            content_attribute (str): le contenu identifiant pour reconnaître
            l'instance

        Returns:
            dict: l'instance de la collection que l'on veut récupérer
        """
        data = self.pdao.get_data(url)

        for i in data:
            if i[attribute] == content_attribute:
                return i


    def filter(self, data_item, research_data):
        """_summary_

        Args:
            data_item (dict): l'essemble des instances d'un item donnée
            de l'API Directus
            research_data (str): données de recherche qui vont servir pour
            le filtre de ce qui sera retourné

        Returns:
            dict: données filtrées de l'item 
        """

        if research_data[0].isupper():
            new_research = research_data[0].lower() + research_data[1:]
        else:
            new_research = research_data[0].upper() + research_data[1:]

        data_item_filter = []
        for i in data_item:
            added = 0
            title = i['title']
            list_tags = i['tags_name']
            room_name = i['room_name']
            if research_data in title or new_research in title:
                if added == 0:
                    data_item_filter.append(i)
                    added += 1
            for tag in list_tags:
                if tag in research_data or tag in new_research:
                    if added == 0:
                        data_item_filter.append(i)
                        added += 1
            if room_name in research_data or room_name in new_research:
                if added == 0:
                    data_item_filter.append(i)
                    added += 1

        return data_item_filter



    def display_impact(self, url: str,impacttype : str):
        """Renvoi la somme des impacts selon un type 

        Args:
            url (str): url servant à afficher les données
            que l'on veut afficher

            impacttype (str): numero du type d'impact : 1=impact communauté, 2=impact fiche
         

        Returns:
            int : sommes des impacts
        """
        
        data = self.pdao.get_data(url)
        qty=0
        for i in data:
            if i['impact_type'] == impacttype:
                qty+=int(i['numerical_data'])
        return qty
    
    def display_impact_now(self):
        #affiche seulement le nombre de jour depuis le 01/01/23
        #il manque à calculer l'impact de la communauté en cumulant les nombres d'user qui ont 
        #adopté les fiches
        #et stocker cette valeur dans directus (pour pas a la calculer tout le temps)
        date_actuelle = datetime.now().date()
        janvier2023 = datetime.strptime('2023-01-01', '%Y-%m-%d').date()
        difference =  date_actuelle-janvier2023 
        return difference.days
    

    
