# -*- coding:Utf-8 -*-

# Author: Nicolas SENAUD
# Mail:   nicolas@senaud.fr
#
# Project: Reco&Follow
# Platform: Nao v4 (Aldebaran)
#
# Description: Module for face learning and name attribution.

# Import libraries.
import sys
import time

from naoqi import ALProxy
from naoqi import ALModule

names = ["Maman", "Papa", "Jean-Jacques", "Arthur", "Félix", "Merlin"]

def learnFaceProcess(self, face_nb):
	# Coupe la reconnaissance pour accéler le process.
	self.fd.enableRecognition(False)

	print "[INFO ] Face learning process ready"

	if face_nb < 6:
		self.tts.say(names[face_nb])
		self.fd.learnFace(names[face_nb])
		print "[INFO ] Face Learned"
		print "[INFO ] Name:",
		print names[face_nb]

		# Incrémente pour attribuer le nom suivant au visage suivant.
		face_nb += 1
	else:
		self.tts.say("Trop de visages pour ma petite tête !")
		print "[ERROR] Too many faces"

	self.fd.enableRecognition(True)
	print "[INFO ] Face learning process finished"

	return 0