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

class MyIntellect(Intellect):

    def __init__(self):
        return super(MyIntellect, self).__init__()

    @Callable
    def log(self, text):
            self.logger.debug(text)

    @Callable
    def out(self, text):
        print(text)
            
    def prepareLogger(self, logger):
        self.logger = logger


class Conversation(object):

    def getNextSentence(self, answer):
        self.logger.info("Input sentence " + answer)
        sentence = Sentence(answer)

        tokenizer = ToktokTokenizer()
        self.tokens = []
        for sent in sent_tokenize(answer, self.language):
            self.tokens.append(tokenizer.tokenize(sent))
        self.logger.info("Generated Tokens "  + utils.listToString(self.tokens))

        sentence.tokens = self.tokens
        self.postag_tokens = []

        for token in self.tokens:
            self.postag_tokens.append(pos_tag(token))

        self.logger.info("Generated POS TAG Tokens " + utils.listToString(self.postag_tokens))

        sentence.postags = self.postag_tokens

        stemmer = SnowballStemmer(self.language, ignore_stopwords=True)
        self.stemmer_text_words = []
        for token in self.tokens:
            for word in token:
                self.stemmer_text_words.append(stemmer.stem(word))

        self.logger.info("Generated Stemmer Tokens " + utils.listToString(self.stemmer_text_words))
        
        sentence.stemmers = self.stemmer_text_words
         
        classifier_greeting = greeting.Greeting()
        sentence.addClass(classifier_greeting.classify(self.stemmer_text_words))
        #print(accuracy(classifier, test_set))


        myIntellect = MyIntellect()
        myIntellect.prepareLogger(self.logger)

        policy_d = myIntellect.learn(myIntellect.local_file_uri("./rulesset/rules.policy"))

        self.context.sentence = sentence 
        myIntellect.learn(self.context)

        myIntellect.reason()

        myIntellect.forget_all()
       

    def dialogue_act_features(self, post):
        features = {}
        for word in word_tokenize(post):
            features['contains({})'.format(word.lower())] = True
        return features

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