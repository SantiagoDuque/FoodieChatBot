# -*- coding: utf-8 -*-
#Clase principal de acceso por consola al bot

from conversation import Conversation
import utils
import actions

def main():

    #Primer dialogo para el saludo inicial
    def  firstDialog(conversation):
        print(u'Bienvenido. ¿Cómo estás?')
        answer = utils.input()
        conversation.getNextSentence(answer, actions.BotActions.GREETING)
        return answer

    print("Prueba bot DASI")
    
    
    conversation = Conversation()
    answer = firstDialog(conversation)

    #Mientras no salgas del dialogo
    while answer.lower() != "exit\n":
        answer = utils.input()
        #se envia lo recogido por consola a nuestra conversacion 
        conversation.getNextSentence(answer)

if __name__ == "__main__":
    main()
