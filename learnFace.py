# -*- coding:Utf-8 -*-

# Author: Nicolas SENAUD
# Mail:   nicolas@senaud.fr
#
# Project: Reco&Follow
# Platform: Nao v4 (Aldebaran)
#
# Description: Main part of a learning and namming face detection module.

# Le module est séparé pour les tests en plusieurs étapes :

# - Effacement de la base de donnée de visages, pour éviter tout conflit ;
# - Attente de l’évènement FaceDetected() [état: idle] ;
# - Apprentissage du visage [état: learn];
# - Association d’un nom au visage [état: name];
# - Dis le nom de la personne [état: say];
# - Repasse en attente d’un nouvel évènement FaceDetected().

# Import Bibliotheques.
import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
from optparse import OptionParser

from LearnFacePackage.learn import learnFaceProcess

# IP du Nao, a adapter avant l'execution.
IP = "192.168.1.10"
# Port standard.
port = 9559

# Variables d'instance.
Detected = None
memory = None

# Variables globales
# Numéro du visage à reconnaître (de 0 à 5)
face_nb = 0

# States: idle, learn, name, say (Cf Description en début de programme).
state = "idle"

# Déclaration de la classe (description de l'objet)
# dans lequel se trouve l'essentiel du code "utile".
class FaceDetectionModule(ALModule):
	# Déclaration de méthode.
	def __init__(self, name):
		ALModule.__init__(self, name)
		
		print "[INFO ] FaceDetectionModule initialization"

		# Instanciation d'un objet tts de classe ALTextToSpeech.
		self.tts = ALProxy("ALTextToSpeech")
		self.tts.setLanguage("french")
		# Instanciation d'un objet tts de classe ALFaceDetection.
		self.fd  = ALProxy("ALFaceDetection")

		# Variable d'instance.
		global memory		
		# Instanciation d'un objet memory de classe ALMemory.
		memory = ALProxy("ALMemory")
		# Appel de la methode subsribeToEvent...
		memory.subscribeToEvent("FaceDetected", 	  # Sur cet evenement...
								"FaceDetection",	  # ...de cet instance...
								"onDetection")		  # ...declancher l'appel
													  # ...de cette methode.
		print "[INFO ] FaceDetectionModule initialized"

	# Méthode appelée sur l'évènement.
	def onDetection(self, *_args):
		print "[INFO ] FaceDetection: Face detected"

		global face_nb
		print "[INFO ] FaceDetection initialize face detection process"
		learnFaceProcess(self, face_nb)


# Main : première fonction exécutée.
def main():
	# À déchiffrer... Mais permet d'employer des paramètres
	# réseau par défaut au sein des déclarations d'objet dans
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
	global FaceDetection
	# Instanciation de l'objet FaceDetection.
	FaceDetection = FaceDetectionModule("FaceDetection")

	# Tourne indéfiniement...
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
