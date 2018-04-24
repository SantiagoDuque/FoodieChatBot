# -*- coding: utf-8 -*-
from conversation import Conversation
import utils

def main():
    print("Prueba bot DASI")
    print(u'Bienvenido. ¿Cómo estás?')
    answer = utils.input()
    conversation = Conversation()
    while answer.lower() != "exit\n":
        conversation.getNextSentence(answer)
        answer = utils.input()

if __name__ == "__main__":
    main()
