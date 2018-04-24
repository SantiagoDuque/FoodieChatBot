# -*- coding: utf-8 -*-
class Context:
    @property
    def sentence(self):
        return self.sentence

    @sentence.setter
    def sentence(self, sentence):
        if self.sentence == None:
            self.sentence = sentence
        else:
            sentence.before = self.sentence
            self.sentence = sentence

    def __init__(self):
        self.sentence = None
        
    def getLastSentence(self):
        return self.sentence

    def lastSentenceContains(self, tokens, type_token):
        sentence = self.getLastSentence()

        if type_token.lower() == "stemmers":
            return all(x in sentence.stemmers for x in tokens)

        if type_token.lower() == "postags" :
            return all(x in sentence.postags for x in tokens)

        if type_token.lower() == "tokens":
            return all(x in sentence.tokens for x in tokens)

   
class Sentence:
    def __init__(self, answer):
        self._tokens = []
        self._postags = []
        self._stemmers = []
        self._answer = answer
        self._categories = ""
        self._before = None
        self._classes = []

    def addClass(self, class_sentence):
        if class_sentence != None:
            self.classes.append(class_sentence)

    @property
    def classes(self):
        return self._classes

    @classes.setter
    def classes(self, value):
        self._classes = value

    @property
    def answer(self):
        return self._answer

    @property
    def tokens(self):
        return self._tokens

    @tokens.setter
    def tokens(self, value):
        self._tokens = value

    @property
    def postags(self):
        return self._postags

    @postags.setter
    def postags(self, value):
        self._postags = value

    @property
    def stemmers(self):
        return self._stemmers

    @stemmers.setter
    def stemmers(self, value):
        self._stemmers = value

    @property
    def before(self):
        return self._before

    @before.setter
    def before(self, value):
        self._before = value

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, value):
        self._categories = value