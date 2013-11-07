# -*- coding:Utf-8 -*-
# Import Bibliotheques.
import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
from optparse import OptionParser

# IP du Nao, a adapter avant l'execution.
IP = "192.168.1.08"
# Port standard.
port = 9559

# Variables d'instance.
TouchMeToSpeak = None
memory = None
etat = 1


# Declaration de la classe (description de l'objet)
# dans lequel se trouve l'essentiel du code "utile".
class TouchMeToSpeakModule(ALModule):
	# Declaration de methode.
	def __init__(self, name):
		ALModule.__init__(self, name)
		
		# Instanciation d'un objet tts de classe ALTextToSpeech.
		self.tts = ALProxy("ALTextToSpeech")

		# Variable d'instance.
		global memory		
		# Instanciation d'un objet memory de classe ALMemory.
		memory = ALProxy("ALMemory")
		# Appel de la methode subsribeToEvent...
		memory.subscribeToEvent("FrontTactilTouched", # Sur cet evenement...
								"TouchMeToSpeak",	  # ...de cet instance...
								"onTouched")		  # ...declancher l'appel
													  # ...de cette methode.

	# Methode appellee sur l'evenement.
	def onTouched(self, *_args):
		# Suppression de l'attente d'evenement...
		# ... Pour eviter un conflit ?
		memory.unsubscribeToEvent("FrontTactilTouched",
								  "TouchMeToSpeak")

		# *** Action principale de la methode ***
		# Ici Nao dit la chaine en parametre de la methode say	
		global etat
		if etat == 1:
			self.tts.setLanguage("french")
			self.tts.setVolume(0.2)
			self.tts.say("Je suis dans le premier état")
			etat = 2
		elif etat == 2:
			self.tts.setLanguage("french")
			self.tts.setVolume(0.2)
			self.tts.say("Je suis dans le second état")
			etat = 1
		
		# ***************************************

		# On se reinscrit a l'evenement.
		memory.subscribeToEvent("FrontTactilTouched",
								 "TouchMeToSpeak",
								 "onTouched")

# Main : premiere fonction executee.
def main():
	# A dechiffrer... Mais permet d'employer des parametres
	# reseau par defaut au sein des declarations d'objet dans
	# le reste du programme...
	parser = OptionParser()
	parser.set_defaults(
		pip = IP,
		pport = 9559)
		
	(opts, args_) = parser.parse_args()
	pip = opts.pip
	pport = opts.pport

	myBroker = ALBroker("myBroker",
						"0.0.0.0",
						0,
						pip,
						pport)
	# ########################################################

	# Variable d'instance.
	global TouchMeToSpeak
	# Instanciation de l'objet TouchMeToSpeak.
	TouchMeToSpeak = TouchMeToSpeakModule("TouchMeToSpeak")

	# Tourne indefiniement...
	try:
		while True:
			time.sleep(1)

	# ...Jusqu'a la production de l'exception interruption clavier.
	except KeyboardInterrupt:
		print
		print "Interrupted by user, shutting down"
		myBroker.shutdown()
		sys.exit(0)

if __name__ == "__main__":
	main()
