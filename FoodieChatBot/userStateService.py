import pandas
import random

class Preference(object):

    def __init__(self):
        self.zipCode = None 
        self.price = None 
        self.type = None 

class UserState(object):
    
    def __init__(self):
        self.zipCodes = None
        self.visited = None
        self.lastVisited = None
        self.lastZipCode = None
        self.lastPrice = None
        self.lastType = None

    def addVisited(self, id):
        if id in self.visited:
            self.visited[id].times += 1
        else:
            self.visited[id] = { 'times' : 0}

        self.lastVisited = id

    def addZipCode(self,zipCode):
        if id in self.visited:
            self.zipCodes[zipCode].times += 1
        else:
            self.zipCodes[zipCode] = { 'times' : 0}

        self.lastZipCode = zipCode

    def addPrice(self, price):
        self.lastPrice = price

    def addType(self, type):
        self.lastType = type

class Suggestion(object):
    def __init__(self, msg, restaurant):
        self.msg = msg
        self.restaurant = restaurant

class SuggestionService(object):

    def __init__(self):
        self.resturants = pandas.read_csv('restaurante.csv', sep=';')
        

    def get(self, userstate, preference):
        
        zipCode = None
        price = None
        type = None
        

        if preference.price == None:
            price = userstate.lastPrice

        if preference.type == None:
            if userstate.lastVisited == None:
                type = None
            else:
                pass

        if preference.zipCode == None and preference.price == None and preference.type == None:

            if userstate.lastType == None and userstate.lastZipCode == None:
                resturant = self.resturants.sample()
                return Suggestion("Vaya... No sabemos nada de ti. Quieres ir a", resturant)

            rand = random.randint(1, 2)

            if userstate.lastType == None and userstate.lastZipCode != None:
                rand = 2
            if userstate.lastType != None and userstate.lastZipCode == None:
                rand = 1

            if rand == 1:
                resturant = self.resturants[self.resturants['categoria'] == userstate.lastType].groupby('categoria').first()
                return Suggestion("Como no tenemos preferencias tuyas te apetece comida de " + userstate.lastType , resturant)
            if rand == 2:
                resturant = self.resturants[self.resturants['zipcode'] == userstate.lastZipCode].groupby('zipcode').first() 
                return Suggestion("Como no tenemos preferencias tuyas te apetece ir cerca de " + str(userstate.lastZipCode), resturant)


        if preference.zipCode != None and preference.price != None and preference.type != None:
            resturant = self.resturants[(self.resturants['categoria'] == preference.type) & (self.resturants['zipcode'] == preference.zipCode) & (self.resturants['precio'] == preference.price)].groupby('zipcode').first() 
            return Suggestion("Como no tenemos preferencias tuyas te apetece ir cerca de " + userstate.lastZipCode, resturant)

        if preference.zipCode != None:

            if  preference.price == None and preference.type == None:
                rand = random.randint(1, 2)

                if userstate.lastType == None and userstate.lastPrice != None:
                    rand = 2
                if userstate.lastType != None and userstate.lastPrice == None:
                    rand = 1

                if userstate.lastType == None and userstate.lastPrice == None:
                    rand = 3

                if rand == 1:
                    resturant = self.resturants[(self.resturants['zipcode'] == preference.zipCode) & (self.resturants['categoria'] == userstate.lastType)].groupby('categoria').first()
                    return Suggestion("Como hace poco querias un sitio de " + userstate.lastType + " y ahora lo quieres cerca de " + str(preference.zipCode), resturant)
                if rand == 2:
                    resturant = self.resturants[(self.resturants['zipcode'] == preference.zipCode) & (self.resturants['precio'] == userstate.lastPrice)].groupby('zipcode').first() 
                    return Suggestion("Como hace poco querias un sitio " + str(userstate.lastZipCode) + " y ahora lo quieres cerca de " + str(preference.zipCode), resturant)
                if rand == 3:
                    resturant = self.resturants[self.resturants['zipcode'] == preference.zipCode].groupby('zipcode').first() 
                    return Suggestion("Como quieres cerca de " + str(preference.zipCode), resturant)


            if  preference.price != None and preference.type == None:
                resturant = self.resturants[(self.resturants['zipcode'] == preference.zipCode) & (self.resturants['precio'] == preference.price)].groupby('zipcode').first() 
                return Suggestion("Como quieres un sitio de precio " + preference.price + " y cerca de " + str(preference.zipCode), resturant)



        resturant = self.resturants.sample()
        return Suggestion("Vaya... No sabemos nada de ti. Quieres ir a", resturant)
            
