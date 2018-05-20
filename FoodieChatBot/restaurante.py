# -*- coding: iso-8859-15 -*-

# Clase para almacenar los datos de contacto de un restaurante
class ContactDetails:

    def __init__(self, email, phone, fax, web):

        self.email = email
        self.phone = phone
        self.fax = fax
        self.web = web

# Clase para almacenar los datos relativos a la ubicación del restaurante
class Address:

    def __init__(self, address, zipcode , latitude, longitude, locality, country):

        self.address = address
        self.zipcode = zipcode
        self.latitude = latitude
        self.longitude = longitude
        self.locality = locality
        self.country = country

# Clase para almacenar los datos de un restaurante
class Restaurante:

    def __init__(self, id, name, contact_details, address, type_of_food, info, price):

        self.id = id
        self.name = name
        self.contact_details = contact_details
        self.address = address
        self.type_of_food = type_of_food
        self.info = info
        self.price = price





