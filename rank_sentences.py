from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.tag import pos_tag
import nltk

def rank_sentences(list_of_sentences, q1, q2, max_sents):
	tokenizer = RegexpTokenizer("\s+", gaps = True)
	list_of_scored_sentences = []
	for sentence_tuple in list_of_sentences:
		sentence = sentence_tuple[1]
		#split sentence in to words
		tokenized_sentence = tokenizer.tokenize(sentence)
		#label parts of speech, returns list of tuples (word, part of speech)
		pos_sentence = nltk.pos_tag(tokenized_sentence)
		score = 0

		# STARTS WITH QUERY (OR SYN) FOLLOWED BY VERB?
		# ____________EDIT THIS WHEN SYNONYMS IMPLEMENTED ___________
		#
		#
		if tokenized_sentence[0] == q1 or tokenized_sentence[0] == [q2]:
		 	if pos_sentence[1][0] == "V":
		 		score +=5

		# PRESENCE OF USER INPUTTED KEYWORDS
		if q1 in sentence or q2 in sentence:
			score += 5
		
		# PRESENCE OF SUGGEST, FOUND, SHOW, DATA
		good_words = [" suggest ", " found ", " show ", " data "]
		if any(word in sentence for word in good_words):
			score += 9

		# PRESENCE OF NOT, LACK, FAIL, WITHOUT
		bad_words = [" not ", " lack ", " fail ", " without "]
		if any(word in sentence for word in bad_words):
			score -=3 

		# TEST SENTENCE LENGTH
		if len(tokenized_sentence) > 30:
			score -= 3

		scored_sentence_tuple = (score, sentence_tuple[0], sentence_tuple[1])
		list_of_scored_sentences.append(scored_sentence_tuple)

	sorted_list_of_scored_sentences = sorted(list_of_scored_sentences, reverse=True)
	#print len(sorted_list_of_scored_sentences)
	pruned_sorted_list_of_scored_sentences = sorted_list_of_scored_sentences[0:max_sents]
	
	return pruned_sorted_list_of_scored_sentences