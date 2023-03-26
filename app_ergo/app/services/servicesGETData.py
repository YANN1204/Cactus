import datetime
from datetime import datetime, timedelta
from calendar import monthrange
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
import pandas as pd

from app.models.dataDAO import DataDAO


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
   


    def display_places(self, url_item: str, urlu: str, urlft: str, urlt: str, urlr: str, urli: str, urlc: str):
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
            if url_item == 'alternative_cards':
                item['impact_details'] = self.instance_by_id(urli, item['impact'])
            else :
                item['comments'] = self.find_comments(item['id'], urlc, urlu)

        return data
    
    """ A VOIR SI MIEUX CAR UTILISE LA METHODE DONNEE PAR LE PROF """
    def display_places2(self, url_item: str, urlu: str, urlft: str, urlt: str, urlr: str):
        data = self.pdao.get_data2(url_item + "?fields=*.*")
        # parcourt la liste d'items du dictionnaire data
        list_dic = []
        for i in data["data"] :
            #print(item)
            item = {}
            item['id'] = i['id']
            item['title'] = i['title']
            item['date_created'] = self.convert_date(i['date_created'])
            item['pseudo'] = i['user_id']['pseudo']
            tags_id = []
            for t in i['tag'] :
                tags_id.append(t['tags_id'])
            item['tags'] = tags_id
            item['room_name'] = i['room_id']['room_name']
            list_dic.append(item)
        return list_dic
    

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


    def display_instance(self, idInstance: str, url_item: str, urlu: str, urlt: str, urlft: str, urlr: str, urlc: str, urli: str):
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
        if url_item == 'alternative_cards':
            data['impact_details'] = self.instance_by_id(urli, data['impact'])
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

    def card_adopted(self, idFiche : str, idUser : str):
        data = self.pdao.get_data("users_alternative_cards")
        found = False
        for d in data:
            #if d['users_id'] == type(None) or d['alternative_cards_id'] == type(None):
            #    found = False
            
            if d['users_id'] == idUser and d['alternative_cards_id'] == idFiche:                
                found = True      
        return found
    
    
    
    def index_users_alternative_cards(self, idFiche : str, idUser : str):
        data = self.pdao.get_data("users_alternative_cards")
        found = "null"
        for d in data:
            if (d['users_id'] == idUser and d['alternative_cards_id'] == idFiche):
                found = d["id"]
                break
        return found
    
    def index_impact(self, idFiche : str, idUser : str):
        #récupération de l'id de l'impact dans la fiche de l'alternative
        data = self.pdao.get_data("alternative_cards")
        idImpact = ""
        for d in data:
            if (d['id'] == idFiche):
                idImpact = d['impact']
                break
        
        #recherche de "sentence_on_data" et "numerical_data" de l'impact dans la table impact
        data = self.pdao.get_data("impacts")
        sentence_on_data = ""
        numerical_data = ""
        for d in data:
            if (d['id'] == idImpact):
                sentence_on_data = d["sentence_on_data"]
                numerical_data = d["numerical_data"]
                break
        #recherche de l'id de l'impact qui posséde user_id , sentence_on_data et nulerical_data dans la table impact
        id_impact_user = ""
        for d in data:
            if (d['user_id'] == idUser and d['sentence_on_data'] == sentence_on_data and d["numerical_data"] ==numerical_data ):
                id_impact_user = d['id']
                break
        
        return id_impact_user

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


    def filter(self, data_item, research_data, type_of_data, room):
        """_summary_

        Args:
            data_item (dict): l'essemble des instances d'un item donnée
            de l'API Directus
            research_data (str): données de recherche qui vont servir pour
            le filtre de ce qui sera retourné
            type_of_data (str): type de données pour les fiche d'alternative : pratique, conseil ou 
            témoignage, forums, articles scientifiques ou tous en même temps

        Returns:
            dict: données filtrées de l'item 
        """
        if len(research_data) != 0:
            if research_data[0].isupper():
                new_research = research_data[0].lower() + research_data[1:]
            else:
                new_research = research_data[0].upper() + research_data[1:]
        else:
            research_data = ""
            new_research = ""

        data_item_filter = []
        for i in data_item:
            added = 0
            title = i['title']
            list_tags = i['tags_name']
            room_name = i['room_name']
            if type_of_data == "forum":
                id_type_of_cards = None
            else:
                id_type_of_cards = i['type_of_card']

            if research_data in title or new_research in title:
                if added == 0:
                    data_item_filter.append(i)
                    added += 1
            for tag in list_tags:
                if tag in research_data or tag in new_research or research_data in tag or new_research in tag:
                    if added == 0:
                        data_item_filter.append(i)
                        added += 1
            if room_name in research_data or room_name in new_research or research_data in room_name or new_research in room_name:
                if added == 0:
                    data_item_filter.append(i)
                    added += 1
            if id_type_of_cards != type_of_data and type_of_data != "Tous" and type_of_data != "forum":
                if added == 1:
                    data_item_filter.pop()
                    added = 0
            if room_name != room and "maison entiere" != room and None != room:
                if added == 1:
                    data_item_filter.pop()
            print(data_item_filter)

        return data_item_filter


    def cards_adopted(self, id: str):
        data = self.pdao.get_data2("users_alternative_cards" + "?fields=*.*")
        list_dic = []
        for i in data["data"] :
            if i['users_id'] and i['users_id']['id'] == id : 
                item = {}
                item['id'] = i['alternative_cards_id']['id']
                item['title'] = i['alternative_cards_id']['title']
                item['room_name'] = self.instance_by_id('rooms', i['alternative_cards_id']['room_id'])['room_name']
                item['tags'] = self.find_tag('alternative_cards_tags', 'tags', i['alternative_cards_id']['tag'])
                if i['alternative_cards_id']['impact'] :
                    item['impact'] = i['alternative_cards_id']['impact']
                list_dic.append(item)
        return list_dic
    
    def cards_suggested(self, id: str):
        data = self.pdao.get_data2("alternative_cards" + "?fields=*.*")
        list_dic = []
        for i in data["data"] :
            if i['user_id'] and i['user_id']['id'] == id : 
                item = {}
                item['id'] = i['id']
                item['title'] = i['title']
                item['room_name'] = i['room_id']['room_name']
                item['date_created'] = self.convert_date(i['date_created'])
                tags_id = []
                for t in i['tag'] :
                    tags_id.append(t['id'])
                item['tags'] = self.find_tag('alternative_cards_tags', 'tags', tags_id)
                list_dic.append(item)
        return list_dic
    

    def user_impacts(self, id: str, urli):
        """Renvoie la liste des impacts d'un utilisateur 

        Args:
            id (str) : id de l'utilisateur     
            urli (str) : url de la collection impacts     

        Returns:
            list : liste des impacts de l'utilisateur
        """
        data = self.pdao.get_data(urli)
        impacts = []
        for d in data:
            if d['user_id'] == id :
                if d['date_created'] :
                    d['date_created'] = self.convert_date(d['date_created'])
                if d['date_end'] :
                    d['date_end'] = self.convert_date(d['date_end'])
                impacts.append(d)
        return impacts
    
    def all_impacts(self, urli):
        """Renvoie la liste des impacts de tous les utilisateurs

        Args:    
            urli (str) : url de la collection impacts     

        Returns:
            list : liste des impacts de tous les utilisateurs
        """
        data = self.pdao.get_data(urli)
        impacts = []
        for d in data:
            if d['impact_type'] == 'use':
                if d['date_created'] :
                    d['date_created'] = self.convert_date(d['date_created'])
                if d['date_end'] :
                    d['date_end'] = self.convert_date(d['date_end'])
                impacts.append(d)
        return impacts
    

    def impact_total_sum(self, urli: str, id=""):
        """Renvoie un dictionnaire des impacts totaux d'un utilisateur pour chaque topic d'impact

        Args:
            id (str) : id de l'utilisateur     
            urli (str) : url de la collection impacts    

        Returns:
            dic : dictionnaire des impacts totaux de l'utilisateur pour eau, co2 et plastique
        """
        if id != "":
            impacts = self.user_impacts(id, urli)
        else :
            impacts = self.all_impacts(urli)
        today = datetime.now()
        tot_eau = 0
        tot_plastique = 0
        tot_co2 = 0
        for i in impacts :
            if i['date_created'] :
                if i['date_end'] :
                    time = (datetime.strptime(i['date_end'], "%d/%m/%Y") - datetime.strptime(i['date_created'], "%d/%m/%Y")).days
                else :
                    time = (today - datetime.strptime(i['date_created'], "%d/%m/%Y")).days
            tot = time * (i['numerical_data']/30.5)
            if i['impact_topic'] == '1' :
                tot_eau += tot
            elif i['impact_topic'] == '2' :
                tot_plastique += tot
            elif i['impact_topic'] == '3' :
                tot_co2 += tot
        tot_impacts = { 'eau': tot_eau, 'plastique': tot_plastique, 'co2': tot_co2}
        return tot_impacts
    
    
    def impact_per_month(self, urli: str, id=""):
        """Renvoie un dictionnaire des dictionnaires des impacts d'un utilisateur pour chaque topic d'impact
           pour les 5 derniers mois, on a donc '0' la key du mois actuel, 'eau' la key pour accéder dans '0'
           à l'impact total de ce mois sur le topic eau

        Args:
            id (str) : id de l'utilisateur     
            urli (str) : url de la collection impacts    

        Returns:
            dic : dictionnaire des dictionnaires des impacts totaux de l'utilisateur pour eau, co2 et plastique
                  pour chacun des 5 derniers mois
        """
        if id != "" :
            impacts = self.user_impacts(id, urli)
        else :
            impacts = self.all_impacts(urli)

        now = datetime.now()
        today = now.strftime("%d/%m/%Y")
        result = {'0': {'eau':0, 'plastique':0, 'co2':0},
                  '1': {'eau':0, 'plastique':0, 'co2':0},
                  '2': {'eau':0, 'plastique':0, 'co2':0},
                  '3': {'eau':0, 'plastique':0, 'co2':0},
                  '4': {'eau':0, 'plastique':0, 'co2':0}, }

        last_months = [datetime.strptime(now.strftime("%m/%Y"), "%m/%Y")]
        months = [now.strftime("%B")]
        for _ in range(0, 4) :
            now = now.replace(day=1) - timedelta(days=1)
            last_months.append(datetime.strptime(now.strftime("%m/%Y"), "%m/%Y"))
            months.append(now.strftime("%B"))

        for i in impacts :
            debut = datetime.strptime(i['date_created'], "%d/%m/%Y")
            if not i['date_end'] :
                i['date_end'] = today
            fin = datetime.strptime(i['date_end'], "%d/%m/%Y")
            month_debut = (datetime.strptime(debut.strftime("%m/%Y"), "%m/%Y"))
            month_fin = (datetime.strptime(fin.strftime("%m/%Y"), "%m/%Y"))
        
            for m in range(len(last_months)) :
                if month_debut == last_months[m] and month_fin == last_months[m] :
                    tot = (fin - debut).days * (i['numerical_data']/30.5)

                elif month_debut == last_months[m] and month_fin >= last_months[m] :
                    last_day = monthrange(month_debut.year, month_debut.month)[1]
                    last_day = str(last_day) + '/' + debut.strftime("%m/%Y")
                    last_day = (datetime.strptime(last_day, "%d/%m/%Y"))
                    tot = (last_day - debut).days * (i['numerical_data']/30.5)

                elif month_debut <= last_months[m] and month_fin == last_months[m] :
                    first_day = last_months[m]
                    tot = (fin - first_day).days * (i['numerical_data']/30.5)

                elif month_debut <= last_months[m] and month_fin >= last_months[m] :
                    first_day = last_months[m]
                    last_day = monthrange(month_debut.year, month_debut.month)[1]
                    last_day = str(last_day) + '/' + debut.strftime("%m/%Y")
                    last_day = (datetime.strptime(last_day, "%d/%m/%Y"))
                    tot = (last_day - first_day).days * (i['numerical_data']/30.5)

                else :
                    tot = 0
 
                if i['impact_topic'] == '1' :
                    result[str(m)]['eau'] = result[str(m)]['eau'] + tot
                elif i['impact_topic'] == '2' :
                    result[str(m)]['plastique'] = result[str(m)]['plastique'] + tot
                elif i['impact_topic'] == '3' :
                    result[str(m)]['co2'] = result[str(m)]['co2'] + tot

        result['months'] = months
        return result
            

    def graph(self, urli, topic, id="") :
        data = self.impact_per_month(urli, id=id)
        eau = []
        plastique = []
        co2 = []
        months = data['months']
        months.reverse()
        for d in data.keys() :
            if d != 'months':
                eau.append(data[d]['eau'])
                plastique.append(data[d]['plastique'])
                co2.append(data[d]['co2'])
        eau.reverse()
        plastique.reverse()
        co2.reverse()

        if topic == "plastique" :
            list_chiffres = plastique
            title = "Le plastique que tu as évité d'acheter"
            ylabel = "Quantité de plastique en kg"
        elif topic == "eau" :
            list_chiffres = eau
            title = "L'eau que tu as économisée"
            ylabel = "Quantité d'eau en l"
        elif topic ==  "co2" :
            list_chiffres = co2
            title = "Le CO2 que tu as évité d'émettre"
            ylabel = "Quantité de CO2 en kg"

        y = list_chiffres
        y = pd.Series(y)
        x_labels = months
        # Plot the figure.
        fig, ax = plt.subplots(layout='constrained')
        ax = y.plot(kind="bar", color="#BC4749")
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_xticklabels(x_labels)
        rects = ax.patches
        # Make some labels.
        labels = [f"{chiffre:.3f}" for chiffre in list_chiffres]
        for rect, label in zip(rects, labels):
            height = rect.get_height()
            ax.text(
                rect.get_x() + rect.get_width() / 2, height, label, ha="center", va="bottom"
            )
        return fig


            
                