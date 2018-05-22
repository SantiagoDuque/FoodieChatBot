# -*- coding: utf-8 -*-
import sys
import logging
import utils
from context import Context
from context import Sentence 
from intellect.Intellect import Intellect
from intellect.Intellect import Callable
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize.toktok import ToktokTokenizer
from nltk import pos_tag, word_tokenize, sent_tokenize
from nltk.classify import accuracy
from classifiers import greeting
from classifiers import preferences
import actions
import pandas
import userStateService
import restaurantService


#clase que forma parte del framework de reglas 
class MyIntellect(Intellect):

    def __init__(self):
        self.preferences = None
        return super(MyIntellect, self).__init__()

    #salida por el log
    @Callable
    def log(self, text):
            self.logger.debug(text)

    #salida por consola
    @Callable
    def out(self, text):
        print(">>" + text)

    @Callable
    def addPreference(self, text):
        self.preferences = text
            
    def prepareLogger(self, logger):
        self.logger = logger


class Conversation(object):


    #metodo para pintar el restaurante sugerido
    def pintaRestaurante(self, restaurant):
        print(">>>>>>>>> Restaurante "+ restaurant.name)
        print(">>>>>>>>> Cerca de "+ restaurant.address.zipcode)
        salida = ">>>>>>>>> Donde hacen comida tipo: "
        for typeFood in restaurant.type_of_food:
            salida += typeFood + " "

        print(salida)
        print(">>>>>>>>> " + restaurant.info[:100] + "...")


    def emiteSugerencia(self):

        #Casos de prueba -->
        #aquipodemos editar el estado anterior de los datos del usuario apra aprender
        #userState.lastType = "Tapas"
        #userState.lastZipCode = 28005
        #<-- Casos de prueba

        suggestionService = userStateService.SuggestionService()

        #obtenemos la sugerencia de nuestro servicio
        suggestion = suggestionService.get(self.context.userState,self.context.preferences)

        #se usar el servicio de resturantes para buscar todos los datos del resturante sugerido
        restaurant_service = restaurantService.ProcesaRestaurantes()

        if len(suggestion.restaurant) == 0:
            print(">>" + "Parece que no hemos encontrado nada acorde a tus preferencias.")
            print(">>" + "Que te pareceria ir a:")
            preference_aux = userStateService.Preference()
            suggestion_aux = suggestionService.get(self.context.userState,preference_aux)
            if len(suggestion_aux.restaurant) == 0:
                self.pintaRestaurante(restaurant_service.getRandom())
            else:
                self.pintaRestaurante(restaurant_service.getById(int(suggestion_aux.restaurant['id'])))
        else:
            print(">>" + suggestion.msg)
            self.pintaRestaurante(restaurant_service.getById(int(suggestion.restaurant['id'])))

    def forceSuggestion(self):
       self.emiteSugerencia()

    def addPreference(self, preference):
        if preference == "caro":
            self.context.preferences.price = "Caro"
        if preference == "medio":
            self.context.preferences.price = "Medio"
        if preference == "barato":
            self.context.preferences.price = "Barato"
        if preference == "zipcode":
            self.context.preferences.zipCode = int(self.context.sentence.tokens[0][-1])


    #meotodo que ejecuta las reglas y clasifica nuestra entrada
    def getNextSentence(self, answer, botAction = actions.BotActions.NONE):

        #para depurar escribimos SUG por consola y emite un sugerencia
        if answer.strip() == "SUG":
            return self.forceSuggestion()


        self.logger.info("Input sentence " + answer)
        sentence = Sentence(answer)
        sentence.botAction = botAction

        #se generan los tokens de la frase -->
        tokenizer = ToktokTokenizer()
        self.tokens = []
        for sent in sent_tokenize(answer, self.language):
            self.tokens.append(tokenizer.tokenize(sent))
        self.logger.info("Generated Tokens "  + utils.listToString(self.tokens))

        sentence.tokens = self.tokens
        #<-- se generan los tokens de la frase


        #se generan los postags de la frase -->
        self.postag_tokens = []

        for token in self.tokens:
            self.postag_tokens.append(pos_tag(token))

        self.logger.info("Generated POS TAG Tokens " + utils.listToString(self.postag_tokens))

        sentence.postags = self.postag_tokens
        #<-- se generan los posttags de la frase

        #se generan los stemmers de la frase -->
        stemmer = SnowballStemmer(self.language, ignore_stopwords=True)
        self.stemmer_text_words = []
        for token in self.tokens:
            for word in token:
                self.stemmer_text_words.append(stemmer.stem(word))

        self.logger.info("Generated Stemmer Tokens " + utils.listToString(self.stemmer_text_words))
        
        sentence.stemmers = self.stemmer_text_words
        #<-- se generan los stemmers de la frase


        #se generar las clases de la frase de entrada -->
        self.classify_sentence(sentence)

        needReClassify = self.context.addSentence(sentence)

        if needReClassify:
            self.context.sentence.classes = []
            self.classify_sentence( self.context.sentence)

        if "suggestion" in sentence.classes:
            return self.forceSuggestion()

        #--> se generar las clases de la frase de entrada


        # se ejecuta el motor de reglas -->
        self.myIntellect = MyIntellect()
        self.myIntellect.prepareLogger(self.logger)

        #se carga el fichero de base de conocimiento
        self.policy_file = self.myIntellect.local_file_uri("./rulesset/rules.policy")
        policy_d = self.myIntellect.learn_policy(self.policy_file)
        policy_applied = self.myIntellect.learn(self.context)

        self.myIntellect.reason()

        self.myIntellect.forget_all()
        
        self.addPreference(self.myIntellect.preferences)
        #<-- se ejecuta el motor de reglas


   #metodo que ejecuta los clasificadores que hemos creado
    def classify_sentence(self, sentence):

        if "?" in sentence.stemmers:
            sentence.userAction = actions.UserActions.REPLY_ASNWER

        if sentence.botAction == actions.BotActions.GREETING:
            classifier_greeting = greeting.Greeting()
            sentence.addClass(classifier_greeting.classify(sentence.stemmers))

        if sentence.botAction == actions.BotActions.NONE:
            preferences_greeting = preferences.Preferences()
            sentence.addClass(preferences_greeting.classify(sentence.stemmers))

        if len(sentence.classes) == 0:
            sentence.addClass("unknown")

    #metodo que parte los tokens en palabras simples
    def dialogue_act_features(self, post):
        features = {}
        for word in word_tokenize(post):
            features['contains({})'.format(word.lower())] = True
        return features

    #metodo que prepara el log
    def prepareLogger(self):
        self.logger = logging.getLogger('Dasi project')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('log.log')
        fh.setLevel(logging.DEBUG)
        #ch = logging.StreamHandler(sys.stderr)
        #ch.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        #ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        #self.logger.addHandler(ch)

    def __init__(self, language="spanish"):
        self.prepareLogger()
        self.language = language
        self.context = Context()
        self.logger.info("Set conversation. Language " + self.language)
