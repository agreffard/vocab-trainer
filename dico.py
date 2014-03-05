#!/usr/bin/python3.3.0
# -*-coding:utf-8-*

DEFAULT_FILE = 'dico'
DEFAULT_WEIGHT = 5

import sys
import random

class Word:
	def __init__(self, lang1, lang2, weight):
		self.lang1 = lang1
		self.lang2 = lang2
		self.weight = weight
		self.nbOcc = 0
		self.nbErr = 0


def initialize_dico(filename, weight=DEFAULT_WEIGHT):

	try:
		file = open(filename, "r")
	except IOError:
		print "Couldn't open the file '%s'." % filename
		exit()

	words = file.read().split("\n")
	while words[-1] == '':
		del words[-1]

	dico = []

	for idx, line in enumerate(words):
		wordList = line.split("\t")
		if len(wordList) != 2:
			print "Error in the dictionary file (line %d)." % idx + 1
			exit()
		word = Word(wordList[0], wordList[1], weight)
		dico.append(word)

	randTab = []  # list of possible indices
	for i in range(len(dico)):
		for j in range(dico[i].weight):
			randTab.append(i)

	return dico, randTab


def end_program(dico):
	text = ["End of the program.\n"]
	to_revise = []
	for ind in range(len(dico)):
		if dico[ind].nbErr != 0:
			to_revise.append("\t%s = %s : %d error%s\n" % (dico[ind].lang2, dico[ind].lang1, dico[ind].nbErr, 's' if dico[ind].nbErr > 1 else ''))
	if to_revise:
		text.append("WORDS TO REVISE:\n")
		text += to_revise
	else:
		text.append("You made no mistake, congrats!! ")
	text.append("See you soon ;)")
	print ''.join(text)
	exit()


def main(filename):

	dico, randTab = initialize_dico(filename)

	print("### VOCABULARY REVISIONS ### (write 'q' to exit the program)")

	while True:

		r = random.randint(0, len(randTab) - 1)
		i = randTab[r]
		dico[i].nbOcc += 1

		lang = random.randint(0, 1)

		print "%s?" % (dico[i].lang1 if lang == 0 else dico[i].lang2)

		transl = None
		while transl is None:
			transl = raw_input("> ")
			if transl == "q":
				end_program(dico)
			else:	
				if (transl == dico[i].lang2 and lang==0) or (transl == dico[i].lang1 and lang==1):
					print "  BRAVO"
					if dico[i].weight>1:
						dico[i].weight-=1
						try:
						    randTab.remove(i)
						except:
						    pass
				else:
					print "  FALSE, the right answer was: %s" % (dico[i].lang2 if lang == 0 else dico[i].lang1)
					dico[i].weight += DEFAULT_WEIGHT
					dico[i].nbErr += 1
					randTab.extend((i for n in range(DEFAULT_WEIGHT)))


if __name__ == '__main__':
	filename = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE
	main(filename)
