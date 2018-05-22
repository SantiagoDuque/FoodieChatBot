from trainset import preferences_train
from nltk.corpus import nps_chat, stopwords
from nltk import NaiveBayesClassifier, classify

#clase para generera el clasificador de preferencias de resturantes
#usa NaiveBayesClassifier

class Preferences():
    def __init__(self):
        self.stopset = list(set(stopwords.words('spanish')))
        self.train()

    #metodo de entramamiento
    def train(self):

        #lee los datos del fichero de entrenamiento
        position_feats = [(self.word_feats(f.split()), 'position') for f in preferences_train.position ]
        type_feats = [(self.word_feats(f.split()), 'type') for f in preferences_train.type ]
        price_feats = [(self.word_feats(f.split()), 'price') for f in preferences_train.price ]
        suggestion_feats = [(self.word_feats(f.split()), 'suggestion') for f in preferences_train.suggestion ]
        #se entrena el clasificador
        self.classifier_preferences = NaiveBayesClassifier.train(position_feats + type_feats + price_feats + suggestion_feats)

    #metodo que parte en palabras que no sean desechables (stopwords)
    def word_feats(self, words):
        return dict([(word, True) for word in words if word not in self.stopset])
    

    #metodo que pasando una frase en tokesn clasifica si es de preferencia
    def classify(self, tokens):

        classes = self.classifier_preferences.prob_classify(self.word_feats(tokens))
        class_generated = self.classifier_preferences.classify(self.word_feats(tokens))

        prob = classes.prob(class_generated)
        samples = classes.samples()
        #hemos decidido que la probilidad minima que aceptamos para el clasificador es un 40%
        min_prob = 0.40
        if prob > min_prob : 
            return class_generated

        return None
