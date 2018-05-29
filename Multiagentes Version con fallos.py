
import os
import sys
import time
import string
import unittest
import spade

host = "127.0.0.1"

class Neuronal_Net(spade.Agent.Agent):

    def _setup(self):
		self.addBehaviour(self.Behaviour1())
		
    class Behaviour1(spade.Behaviour.OneShotBehaviour):

        def _process( ):
		
            mensaje = spade.ACLMessage.ACLMessage()

            mensaje.addReceiver(spade.AID.aid("b@"+host,["xmpp://b@"+host]))
            mensaje.setContent(NULL)
			
            self.myAgent.send(mensaje)
            print("Se supone que ya las variables fueron enviadas")
            print(mensaje.getContent())
            
        
class Fuzzy(spade.Agent.Agent):
    
    class Behaviour2(spade.Behaviour.EventBehaviour):

        def _process(self):
            mensaje = self._receive(block=True,timeout=10)
            print(mensaje.getContent())
    
    def _setup(self):
        template = spade.Behaviour.ACLTemplate()
        template.setSender(spade.AID.aid("a@"+host,["xmpp://a@"+host]))
        temp = spade.Behaviour.MessageTemplate(template)
        
        self.addBehaviour(self.Behaviour2(),temp)
  
a = Neuronal_Net("a@"+host,"secret")
b = Fuzzy("b@"+host,"secret")



time.sleep(5)
a.start()
b.start()

alive = True

while alive:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        alive=False
		
a.stop()
b.stop()
sys.exit(0)
