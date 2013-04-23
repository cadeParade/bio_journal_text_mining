import pfp
import unicodedata
import re
import nltk


""" takes in a list of sentence tuples
	(ranked score, originating paper id, sentence)
	returns sentences with classification """


class Sentence(object):

	def __init__(self):
		self.paper_id = None
		self.sentence = None
		
		self.tree = None
		
		self.pos_list = []
		self.q1_indexes = []
		self.q2_indexes = []
		self.s_indexes = []
		self.vp_indexes = []

		self.different_clauses = False
		self.vp_between_queries = False
		self.stimulatory_words_present = None
		self.inhibitory_words_present = None
		self.negation_words_present = None
		
		self.stimulatory = False
		self.inhibitory = False
		self.neutral = False
		self.parallel = False
		self.abstract_coocurrence_only = False


	def make_tree(self, sentence):
		"""Takes a sentence and creates a parse tree with pfp """
		parsed_sentence = pfp.Parser().parse(sentence)
		tree = nltk.ImmutableTree.parse(parsed_sentence)
		#tree.draw()
		return tree	


	def traverse(self, t):
		""" given a parse tree, traverses each node and leaf
			and makes an ordered list of each entity of interest
			(query terms, 'S' (notates clauses), and 'VP's (verb phrase)
			also creates lists of indexes of each type of thing in list """
		s_find = re.compile("^S")
		vp_find = re.compile("^VP")
		try:
			t.node
		except AttributeError:
			if "DAT" in t:
				self.pos_list.append(t)
				# adds index of this DAT to q1 index list
				pos_length = len(self.pos_list)
				self.q1_indexes.append(pos_length-1)
			elif "ADHD" in t:
				self.pos_list.append(t)
				pos_length = len(self.pos_list)
				self.q2_indexes.append(pos_length-1)

		else:
	        # Now we know that t.node is defined
	        # Then tests for presence of regex match object 
	        # for clause (S) and verb phrase(VP)
			if s_find.match(t.node):
				self.pos_list.append(t.node)
				pos_length = len(self.pos_list)
				self.s_indexes.append(pos_length-1)
			elif vp_find.match(t.node):
				self.pos_list.append(t.node)
				pos_length = len(self.pos_list)
				self.vp_indexes.append(pos_length-1)
			for child in t:
				self.traverse(child) 


	def is_pos_between(self, q_index_list, pos_indexes):
		"""Given two numbers in a list, tests if any indexes of
			pos_indexes are between the first two numbers """ 
		is_pos_between_queries = any(pos_idx in range(q_index_list[0], q_index_list[1]) for pos_idx in pos_indexes)
		return is_pos_between_queries
	

	def find_the_things(self,q1_indexes, q2_indexes, vp_indexes, s_indexes):
		"""Labels sentence properties of whether s between or vp between
			are true or false """ 
		for idxq1 in q1_indexes:
			for idxq2 in q2_indexes:
				index_list = [idxq1, idxq2]
				index_list.sort()
				if self.is_pos_between(index_list, s_indexes):
					self.different_clauses = True
					break	    	
			for idxq2 in q2_indexes:
				index_list = [idxq1, idxq2]
				index_list.sort()
				if self.is_pos_between(index_list, vp_indexes):
					self.vp_between_queries = True
					break

		print self.pos_list
		print self.different_clauses, "is s between"
		print self.vp_between_queries, "is vp between"
		  

	def test_for_presence_of_words(self, sentence):
		stimulatory_words = ["bind", "binds", "additive", "relationship", 
							 "behavior", "modification", "modify", "modifies"]
		inhibitory_words = ["inactivate", "abolish", "attenuate", "block", "decrease", "eliminate", 
							"inhibit", "inhibits", "reduce", "supress", "supresses"]
		negation_words = [" not ", " no ", " none ", " did not ", " does not "]
		
		#booleans
		self.stimulatory_words_present = any(word in sentence for word in stimulatory_words)
		self.inhibitory_words_present = any(word in sentence for word in inhibitory_words)
		self.negation_words_present = any(word in sentence for word in negation_words)


	def sanitize_sentence(self, sentence):
		""" Supposedly gets rid of sentence formatting that
			will break the program..."""
		
		#converts to ascii
		if isinstance(sentence, unicode):
			sentence = sentence.encode("ascii", "ignore")
		
		#takes out restricted (R) sign
		if "\xc2\xae" in sentence:
			sentence = sentence.replace("\xc2\xae", "")
		
		if "()" in sentence or "( )" in sentence:
			sentence = sentence.replace("()", "")
			sentence = sentence.replace("( )", "")
		
		if len(re.findall(r'\w+', sentence)) > 38:
			sentence = ""

		self.sentence = sentence
		
		# test for "()" or "( )" and delete that if present
		
	def decision_time(self, sentence):
		#test for verb phrase between queries
		if sentence.vp_between_queries == True:
			
			#test for different clauses
			if sentence.different_clauses == True:
				sentence.parallel = True
			else:
				#test for negation
				if sentence.negation_words_present == True:
					sentence.parallel = True
				else:
					#test for telling words
					if sentence.stimulatory_words_present == True:
						sentence.stimulatory = True
					if sentence.inhibitory_words_present == True:
						sentence.inhibitory = True
					else:
						sentence.neutral = True
		#if no verb phrase between query words
		else:
			# test for presence of telling words
			if sentence.stimulatory_words_present == True:
				sentence.stimulatory = True
			elif sentence.inhibitory_words_present == True:
				sentence.inhibitory = True
			else:
				sentence.abstract_coocurrence_only = True


def make_sentence_objects(list_of_sentences, q1, q2):
	"""takes in list of sentences, does some stuff, returns list of populated sentence objects"""
	# print list_of_sentences
	sentence_list = []
	for i, sentence in enumerate(list_of_sentences):
		print sentence[0], "score"
		print sentence[2]

		
		sentence_obj = Sentence()
		sentence_obj.paper_id = sentence[1]
		sentence_obj.sentence = sentence[2]
		sentence_obj.sanitize_sentence(sentence_obj.sentence)
		sentence_obj.tree = sentence_obj.make_tree(sentence_obj.sentence)
		sentence_obj.traverse(sentence_obj.tree)
		sentence_obj.find_the_things(sentence_obj.q1_indexes, sentence_obj.q2_indexes, 
									 sentence_obj.vp_indexes, sentence_obj.s_indexes)
		sentence_obj.test_for_presence_of_words(sentence_obj.sentence)
		sentence_obj.decision_time(sentence_obj)

		sentence_list.append(sentence_obj)

		# print sentence_obj.stimulatory_words_present, "STIM"
		# print sentence_obj.inhibitory_words_present, "INHIBIT"
		# print sentence_obj.negation_words_present, "NEGATION" 

		print sentence_obj.stimulatory, "STIm class"
		print sentence_obj.inhibitory, "inhibitory class"
		print sentence_obj.neutral, "neutral class"
		print sentence_obj.parallel, "parallel class"
		print sentence_obj.abstract_coocurrence_only, "coocurrence only class" 

		
	return sentence_list


def main(scored_sentences, q1, q2):

	sentence_list = make_sentence_objects(scored_sentences, q1, q2)
	print len(sentence_list)
	count_stim = 0
	count_inhib = 0
	count_neutral = 0
	count_parallel = 0
	count_abstract = 0
	for sentence in sentence_list:
		if sentence.stimulatory == True:
			count_stim += 1
		if sentence.inhibitory == True:
			count_inhib += 1
		if sentence.neutral == True:
			count_neutral += 1
		if sentence.parallel == True:
			count_parallel += 1
		if sentence.abstract_coocurrence_only == True:
			count_abstract += 1
	print count_stim, "stim"
	print count_inhib, "inhib"
	print count_neutral, "neutral"
	print count_parallel, "parallel"
	print count_abstract, "abstract"



	
		