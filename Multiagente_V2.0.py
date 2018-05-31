
import os
import sys
import time
import string
import unittest
import commands
import time
import spade

host = "127.0.0.1"

class NeuralNet(spade.Agent.Agent):

    def _setup(self):
		self.addBehaviour(self.NeuralNetMsgBehav())
		print "Launcher started"
		
    class NeuralNetMsgBehav(spade.Behaviour.OneShotBehaviour):

        def _process(self):

            mens = spade.ACLMessage.ACLMessage()
            mens.setPerformative("inform")
            mens.addReceiver(spade.AID.aid("b@"+host,["xmpp://b@"+host]))

            i = 0
            #Porque solo tenemos 3 entradas válidas
            while i == 0:
                NroHijos = MetodoAnticonceptivo = input("Que metodo anticonceptivo utiliza?, 1: ninguno, 2: corto plazo, 3: largo plazo: ")
                if NroHijos > 3:
                    print("Ingrese un número del 1 al 3")
                else:
                    i = 1
                    
            NroHijos = input("Cuantos hijos tiene la familia?: ")
            Edad = input("Que edad tiene la esposa?: ")
            mens.setContent([MetodoAnticonceptivo, NroHijos, Edad])#aca hay que poner los dados de caudales de entrada 
            self.myAgent.send(mens)
            print("Entradas al fuzificador:")
            print(mens.getContent())
            
                        
            
class Fuzzy(spade.Agent.Agent):
    
    class FuzzyMsgBehav(spade.Behaviour.EventBehaviour):

        def _process(self):
            mens = self._receive(block=True,timeout=10)
            print "La fuzzy dice que el mensaje fue recivido y es:"
            print(mens.getContent())
            print("aqui no he podido ver como hace uno para pasar estos atributos de forma que no sea como pasando atributos a una clase")
    
    def _setup(self):
        template = spade.Behaviour.ACLTemplate()
        template.setSender(spade.AID.aid("a@"+host,["xmpp://a@"+host]))
        t = spade.Behaviour.MessageTemplate(template)
        
        self.addBehaviour(self.FuzzyMsgBehav(),t)
        
    
#IMPORTANTE, NO TOCAR  :V   
Neural_Net = NeuralNet("a@"+host,"secret")
VarFuzz = Fuzzy("b@"+host,"secret")

#Ahora iniciamos los agentes, se le puede hacer sleep ero no hace falta

VarFuzz.start()
#aqui venia un sleep por default pero veo que no es necesario
Neural_Net.start()

alive = True

while alive:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        alive=False
        
Neural_Net.stop()
VarFuzz.stop()
sys.exit(0)
