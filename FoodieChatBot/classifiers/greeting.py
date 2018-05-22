from trainset import greeting_train
from nltk.corpus import nps_chat, stopwords
from nltk import NaiveBayesClassifier, classify


#clase para generera el clasificador de saludo normal
#usa NaiveBayesClassifier


class Greeting():
    def __init__(self):
        self.stopset = list(set(stopwords.words('spanish')))
        self.train()

    #metodo de entramamiento
    def train(self):
        #lee los datos del fichero de entrenamiento
        pos_feats = [(self.word_feats(f.split()), 'greeting_positive') for f in greeting_train.positive ]
        neg_feats = [(self.word_feats(f.split()), 'greeting_negative') for f in greeting_train.negative ]
        #se entrena el clasificador
        self.classifier_greeting = NaiveBayesClassifier.train(pos_feats + neg_feats)

    #metodo que parte en palabras que no sean desechables (stopwords)
    def word_feats(self, words):
        return dict([(word, True) for word in words if word not in self.stopset])
    
    #metodo que pasando una frase en tokesn clasifica si es de preferencia
    def classify(self, tokens):

        classes = self.classifier_greeting.prob_classify(self.word_feats(tokens))
        class_generated = self.classifier_greeting.classify(self.word_feats(tokens))

        prob = classes.prob(class_generated)
        samples = classes.samples()
        min_prob = 1.0 / len(samples)
        #hemos decidido que la probilidad minima que aceptamos para el clasificador es un 50% (solo tenemos dos clases)
        if prob > min_prob : 
            return class_generated

        return None
