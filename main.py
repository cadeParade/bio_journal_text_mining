import make_syn_dict, get_info_from_xml, rank_sentences, decide_classification, query_class_def
import nltk, pfp, unicodedata, re
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.tag import pos_tag
import do_something_with_the_database

class Paper(object):

	def __init__(self):
		self.id = None
		self.parsed = None
		self.title = None
		self.authors = None
		self.mesh_terms = None
		self.abstract = None
		self.all_sentences = None
		#classified sentences is a list of sentence objects
		self.classified_sentences = []
		self.word_tokenized = None
		#list of tuples (sentence, pos in abstract)
		self.coocurring_sentences = None
		#list of tuples (sentence, pos in abstract)
		self.non_interactive_sents = None

	def make_sentence_id_tuples(self, coocurring_sentences):
		""" makes list of tuples of sentences in format
			(paper_id, sentence, order in absract) """
		list_of_tuples = []
		for sentence in coocurring_sentences:
			current_tuple = (self.id, sentence[0], sentence[1])
			list_of_tuples.append(current_tuple)
		return list_of_tuples


	def split_abstract_into_sentences(self, query):
		""" splits abstracts on periods and discards any 
			sentence where both queries do not appear """
		sentence_list = []
		sentence_list.append(self.title)
		if self.abstract:
			abstract_sentence_split = self.abstract.split(".")
			sentence_list.extend(abstract_sentence_split)

		self.all_sentences = sentence_list


	def find_query_in_sentence(self, sentence, query_str, syns_list):
		if sentence:
			if query_str in sentence:
				return True
			else:
				if syns_list:
					for syn in syns_list:
						if syn in sentence:
							return True
				else:
					return False


	def find_sentences_with_both_queries(self, sentence_list, query):
		"""takes list of sentences, tests if both queries are in each 
			sentence. If so, keeps, if not, adds to non-interactive list"""
		coocurrence_list = []
		non_interactive_list = []
		for i, sentence in enumerate(sentence_list):
			q1_or_syns_found = self.find_query_in_sentence(sentence, query.q1, query.q1_syns_checked)
			q2_or_syns_found = self.find_query_in_sentence(sentence, query.q2, query.q2_syns_checked)
			if q1_or_syns_found and q2_or_syns_found:
				sentence_and_position = (sentence, i)
				coocurrence_list.append(sentence_and_position)
			elif q1_or_syns_found or q2_or_syns_found:
				sentence_and_position = (sentence, i)
				non_interactive_list.append(sentence_and_position)
		self.non_interactive_sents = non_interactive_list
		return coocurrence_list

	def word_tokenize(self):
		""" splits sentences into list of words by spaces """
		tokenizer = RegexpTokenizer("\s+", gaps = True)

		if self.coocurring_sentences:
			self.word_tokenized = []
			for sentence in self.coocurring_sentences:
				tokenized_words =  tokenizer.tokenize(sentence[0])
				self.word_tokenized.append(tokenized_words)
		else:
			self.word_tokenized = None

	# def convert_unicode_to_ascii(self,unicode_string):
	# 	""" pfp can't handle UNICODE even though it took
	# 		so long to install it because of something
	# 		related to UNICODE. I don't even think this 
	# 		is used in this class anymore. """ 
	# 	unicode_string = unicode_string.encode("ascii", "ignore")
	# 	return unicode_string


def make_paper_objects(dict_of_info):
	"""takes in dict of info, returns dictionary paper objects like
		["paper_id#"]: paper object """
	paper_dict = {}

	if "existing_id_list" in dict_of_info: 
		ids = dict_of_info["existing_id_list"]

		print ids, "IDSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"
		for pubmed_id in ids:
			local_paper = do_something_with_the_database.get_paper_info(pubmed_id)
			paper = Paper()
			paper.id = local_paper.pubmed_id
			paper.title = local_paper.title
			abstract_of_sent_db_obj = do_something_with_the_database.assemble_abstract(paper.id) 
			paper.all_sentences = []
			for sentence in abstract_of_sent_db_obj:
				paper.all_sentences.append(sentence.sentence)
			paper.authors = local_paper.authors
			paper_dict[pubmed_id] = paper
	
	if "fetched_dict_of_info" in dict_of_info:		
		fetched_id_list = dict_of_info["fetched_dict_of_info"]["fetched_id_list"]
		title_list = dict_of_info["fetched_dict_of_info"]["title_list"]
		abstract_list = dict_of_info["fetched_dict_of_info"]["abstract_list"]
		authors_list = dict_of_info["fetched_dict_of_info"]["authors_list"]

		for i, paper_id in enumerate(fetched_id_list):
			paper = Paper()
			paper.id = fetched_id_list[i]
			paper.title = title_list[i]
			paper.abstract = abstract_list[i]
			paper.authors = authors_list[i]
			paper_dict[paper_id] = paper
	
	return paper_dict

		
def get_list_of_all_sentences(paper_dict, query):
	""" populates paper class properties
	# extracts list of all coocurring sentences """
	list_of_sentences = []
	for key in iter(paper_dict):
		if not paper_dict[key].all_sentences:
			paper_dict[key].split_abstract_into_sentences(query)
			paper_dict[key].word_tokenize()
			coocurrence_list = paper_dict[key].find_sentences_with_both_queries(paper_dict[key].all_sentences, query)
			sentence_list = paper_dict[key].make_sentence_id_tuples(coocurrence_list)
			list_of_sentences.extend(sentence_list)
			
		else: 
			coocurrence_list = paper_dict[key].find_sentences_with_both_queries(paper_dict[key].all_sentences,query)
			sentence_list = paper_dict[key].make_sentence_id_tuples(coocurrence_list)
			list_of_sentences.extend(sentence_list)
	
	return list_of_sentences


def assign_sentences_back_from_which_they_came(paper_dict, classified_sentence_list):
	#assigns classified sentences back to paper from which it came
	for sentence in classified_sentence_list:
		paper_dict[sentence.paper_id].classified_sentences.append(sentence)




def main(query):
	# q1 = "DAT"
	# q2 = "ADHD"

	# max_num_sents_to_analyze = 23
	max_num_articles_to_get = 100
	# syn_dict_location = "corpus_or_database/chilibot.syno.database"

	# retreives info from pubmed
	dict_of_info = get_info_from_xml.main(query, max_num_articles_to_get)
	# puts papers into objects
	paper_dict = make_paper_objects(dict_of_info)

	return paper_dict



