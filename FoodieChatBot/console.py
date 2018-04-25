# -*- coding: utf-8 -*-
from conversation import Conversation
import utils
import actions

def main():

    def  firstDialog(conversation):
        print(u'Bienvenido. ¿Cómo estás?')
        answer = utils.input()
        conversation.getNextSentence(answer, actions.BotActions.GREETING)
        return answer

    print("Prueba bot DASI")
    
    conversation = Conversation()
    answer = firstDialog(conversation)
    while answer.lower() != "exit\n":
        answer = utils.input()
        conversation.getNextSentence(answer)

if __name__ == "__main__":
    main()
