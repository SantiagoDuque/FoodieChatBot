# -*- coding: utf-8 -*-

from lxml import etree
import restaurante
import re
import random

class ProcesaHTML:

      #Elimina las etiquetas html de un texto
      def elimina_etiquetas_html(self, value):
            return re.sub(r'<[^>]*?>', '', value)

      #Corrige el error de codificaciÃ³n &nbsp por un espacio en blanco
      def eliminaElementosDeProcesamiento(self, value):
          return re.sub(r'&nbsp;', ' ', value);

      def corrigeNombre(self, value):
          value = re.sub(r'&aacute;', 'Ã¡', value)
          value = re.sub(r'&Aacute;', 'Ã', value)
          value = re.sub(r'A&acute;', 'A\'', value)
          value = re.sub(r'&eacute;', 'Ã©', value)
          value = re.sub(r'e&acute;', 'e\'', value)
          value = re.sub(r'&Eacute;', 'Ã', value)
          value = re.sub(r'&iacute;', 'Ã­', value)
          value = re.sub(r'&Iacute;', 'Ã', value)
          value = re.sub(r'&oacute;', 'Ã³', value)
          value = re.sub(r'&ograve;', 'Ã²', value)
          value = re.sub(r'&Oacute;', 'Ã', value)
          value = re.sub(r'o&acute;', 'o\'', value)
          value = re.sub(r'O&acute;', 'O\' ', value)
          value = re.sub(r'&uacute;', 'Ãº', value)
          value = re.sub(r'&ugrave;', 'Ã¹', value)
          value = re.sub(r'&uuml;', 'ÃŒ', value)
          value = re.sub(r'&uacute;', 'Ã', value)
          value = re.sub(r'&ntilde;', 'Ã±', value)
          value = re.sub(r'&Ntilde;', 'Ã', value)
          value = re.sub(r'&rsquo;', '\'', value)
          value = re.sub(r'&amp;', '&', value)
          value = re.sub(r'&ecirc;', 'Ãª', value)
          value = re.sub(r'&ordm;', 'Âº', value)
          value = re.sub(r'&ordf;', 'Âª', value)
          value = re.sub(r'&ndash;', '-', value)
          value = re.sub(r'&iexcl;', 'Â¡', value)

          return value

      def corregirNombresEncoding(self, value):
          #value = re.sub(r'\'xe1', 'Ã¡', value)
          #value = re.sub(r'\xf1', 'Ã±', value)
          print(sys.getdefaultencoding())
          print('previous value')
          print(value)
          #value = value.decode('iso8859-15').encode('utf8')
          #print('encoded value')
          #print(value)
          return value



class ExtraeRestaurantes:

      #Realiza la extracciÃ³n de datos del fichero fuente xml
      def extraeInfo(self):
            doc = etree.parse('restaurantes_v1_es.xml')  # abrimos el xml
            raiz = doc.getroot()  # cogemos el elemento raiz

            # cogemos los atributos dentro del elemento 'service' con su valor, en este caso seran fechaActualizacion e id
            """for attr, value in libro.items():
                  print(attr, value)"""

            #restaurantes = []
            restaurantes = list()


            for elemento in raiz:

                id = elemento.get("id")

                name = elemento.find("basicData/name").text
                #print(name.encode('iso-8859-15'))
                #print(name)
                #print(ProcesaHTML.corrigeNombre(name))

                #insertamos un precio

                price = 0
                #print(name)
                # print(re.findall(r'^[ACEGIKMPQSUWY]', name))
                result = re.match(r'^[ACEGKMPQSWY]', name)
                result2 = re.match(r'^[BDFJLNOTVZ]', name)
                result3 = re.match(r'^[HIRUX]', name)
                if result:
                    #print(result.group(0))
                    #print(10)
                    price = 10
                elif result2:
                    #print(result2.group(0))
                    #print(25)
                    price = 25
                elif result3:
                    #print(result3.group(0))
                    #print(50)
                    price = 50
                else:
                    #print(70)
                    price = 70

                email = elemento.find("basicData/email").text
                phone = elemento.find("basicData/phone").text
                fax = elemento.find("basicData/fax").text
                web = elemento.find("basicData/web").text

                info = elemento.find("basicData/body").text
                # procesamos el texto para eliminar las etiquetas html
                procesaHTML = ProcesaHTML()
                info = procesaHTML.elimina_etiquetas_html(info)
                #info = procesaHTML.eliminaElementosDeProcesamiento(info)
                #info = procesaHTML.corrigeNombre(info)

                address = elemento.find("geoData/address").text
                codigo_postal = elemento.find("geoData/zipcode").text
                latitude = elemento.find("geoData/latitude").text
                longitude = elemento.find("geoData/longitude").text
                locality = elemento.find("geoData/locality").text
                country = elemento.find("geoData/country").text

                categorias = elemento.find("extradata/categorias/categoria/subcategorias")
                # print(categorias[0][1].text)
                # print(len(categorias))


                # type_of_food = list()
                type_of_food = []

                #print(sys.getdefaultencoding())
                if categorias is not None:
                    for categoria in categorias:
                        #typeFood = categoria[1].text
                        #print(typeFood)
                        #type_of_food.append(procesaHTML.corregirNombresEncoding(typeFood))

                        type_of_food.append(categoria[1].text.lower())
                        #print(categoria[1].text)
                else:
                    categoria = elemento.find("extradata/categorias/categoria")
                    if categoria is not None:
                        #typeFood = categoria[1].text
                        #print(typeFood)
                        #type_of_food.append(procesaHTML.corregirNombresEncoding(typeFood))

                        type_of_food.append(categoria[1].text.lower())
                        #print(categoria[1].text)
                    else:
                        type_of_food.append("sin clasificar")

                # print(type_of_food)


                # Creamos un objeto restaurante con los objetos obtenidos del xml
                details = restaurante.ContactDetails(email, phone, fax, web)
                addressR = restaurante.Address(address, codigo_postal, latitude, longitude, locality, country)
                r = restaurante.Restaurante(id, name, details, addressR, type_of_food, info, price)
                restaurantes.append(r)

            return restaurantes

class ProcesaRestaurantes:

    e = ExtraeRestaurantes()
    res = e.extraeInfo()

    # si al constructor no le pasamos argumentos tomarÃ¡ por defecto el valor de la variable 'res'
    def __init__(self, restaurantes=res):
        self.restaurantes = restaurantes


    def getById(self, id):

        #e = ExtraeRestaurantes()
        #restaurantes = e.extraeInfo()
        restaurantes = self.restaurantes
        r = 0   #serÃ¡ el valor a devolver. Si el restaurante no existe devolverÃ¡ 0, si existe devolverÃ¡ el restaurante
        for i in restaurantes:
            if int(i.id) == id:
                r = i
        return r

    def getByName(self, name):
        # e = ExtraeRestaurantes()
        # restaurantes = e.extraeInfo()
        restaurantes = self.restaurantes
        r = 0  # serÃ¡ el valor a devolver. Si el restaurante no existe devolverÃ¡ 0, si existe devolverÃ¡ el restaurante
        for i in restaurantes:
            if i.name == name:
                r = i
        return r

    def getByTypeOfFood(self, type_of_food):
        # e = ExtraeRestaurantes()
        # restaurantes = e.extraeInfo()
        restaurantes = self.restaurantes
        restaurantes_candidatos = []  # lista con los restaurantes que cocinen un tipo de comida. Si no hay la lista devuelta estarÃ¡ vacia
        for i in restaurantes:
            for tipo_comida in i.type_of_food:
                #print(tipo_comida)
                if tipo_comida == type_of_food:
                    restaurantes_candidatos.append(i)
        return restaurantes_candidatos

    def getByAddress(self, address):
        # e = ExtraeRestaurantes()
        # restaurantes = e.extraeInfo()
        restaurantes = self.restaurantes
        restaurantes_candidatos = []  # lista con los restaurantes que cocinen un tipo de comida. Si no hay la lista devuelta estarÃ¡ vacia
        for i in restaurantes:
            #print(i.address.address)

            #si la direcciÃ³n introducida es aproximadamente la guardada en la BD
            if address.lower() in i.address.address.lower():
                restaurantes_candidatos.append(i)
                print(i.address.address)
        return restaurantes_candidatos

    def getByPrice(self, price):
        # e = ExtraeRestaurantes()
        # restaurantes = e.extraeInfo()
        restaurantes = self.restaurantes
        restaurantes_candidatos = []  # lista con los restaurantes que se encuentren dentro de un rango de precios. Si no hay la lista devuelta estarÃ¡ vacia
        for i in restaurantes:
            # print(i.price)

            # si el precio se encuentra dentro del rango
            if price.lower() == 'barato' or price.lower() == 'economico' or price.lower() == 'econÃ³mico':
                if 0 < i.price <= 15:
                    restaurantes_candidatos.append(i)
            if price.lower() == 'normal' or price.lower() == 'standard' or price.lower() == 'intermedio':
                if 15 < i.price <= 35:
                    restaurantes_candidatos.append(i)
            if price.lower() == 'caro' or price.lower() == 'muy caro':
                if 35 < i.price:
                    restaurantes_candidatos.append(i)
        return restaurantes_candidatos


    def getRandom(self):
        rand = random.randint(1, len(self.restaurantes))
        return self.restaurantes[rand]
