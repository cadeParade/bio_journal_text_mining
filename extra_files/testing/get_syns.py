

from nltk.corpus import wordnet as wn
from sys import argv

script, word = argv

print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

inhibit_synsets = wn.synsets(word)
print inhibit_synsets

for synset in inhibit_synsets:
	current_set = synset
	print current_set
	# for my_set in current_set:
	print current_set.hyponyms()
	print current_set.hypernyms()
	
	for lemma in current_set.lemmas:
		print lemma.derivationally_related_forms()
	# # current_lemmas = [lemma.name for lemma in current_set.lemmas]	
	# print current_lemmas
		
	# for lemma in current_lemmas:
	# 	print lemma.hyponyms()
	# 	print lemma.hypernyms()
	# 	print lemma.derivationally_related_forms()