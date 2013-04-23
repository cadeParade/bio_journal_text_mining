import make_syn_dict, get_info_from_xml, rank_sentences, decide_classification
import nltk, pfp, unicodedata, re
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.tag import pos_tag

class Query(object):

	def __init__(self):
		self.q1 = None
		self.q2 = None

	def make_list_of_all_sentences(self):
		pass

	def pair_sentences_with_paper_id(self):
		pass


class Paper(object):

	def __init__(self):
		self.id = None
		self.parsed = None
		self.abstract = None
		self.all_sentences = None
		self.word_tokenized = None
		self.coocurring_sentences = None
		self.non_interactive_sents = None

	def make_sentence_id_tuples(self):
		""" makes list of tuples of sentences in format
			(paper_id, sentence) """
		list_of_tuples = []
		for sentence in self.coocurring_sentences:
			current_tuple = (self.id, sentence)
			list_of_tuples.append(current_tuple)
		return list_of_tuples


	def split_abstract_into_sentences(self, q1, q2):
		""" splits abstracts on periods and discards any 
			sentence where both queries do not appear """
		sentence_list = []
		sentence_list.append(self.title)
		abstract_sentence_split = self.abstract.split(".")
		sentence_list.extend(abstract_sentence_split)

		self.all_sentences = sentence_list

		coocurrence = self.find_sentences_with_both_queries(sentence_list, q1, q2)
		self.coocurring_sentences = coocurrence

	def find_sentences_with_both_queries(self, sentence_list, q1, q2):
		"""takes list of sentences, tests if both queries are in each 
			sentence. If so, keeps, if not, adds to non-interactive list"""
		coocurrence_list = []
		non_interactive_list = []

		for sentence in sentence_list:
			if q1 in sentence and q2 in sentence:
				coocurrence_list.append(sentence)
			elif q1 in sentence or q2 in sentence:
				non_interactive_list.append(sentence)
		self.non_interactive_sents = non_interactive_list
		return coocurrence_list

	def word_tokenize(self):
		""" splits sentences into list of words by spaces """
		tokenizer = RegexpTokenizer("\s+", gaps = True)

		if self.coocurring_sentences:
			self.word_tokenized = []
			for sentence in self.coocurring_sentences:
				tokenized_words =  tokenizer.tokenize(sentence)
				self.word_tokenized.append(tokenized_words)
		else:
			self.word_tokenized = None

	def convert_unicode_to_ascii(self,unicode_string):
		""" pfp can't handle UNICODE even though it took
			so long to install it because of something
			related to UNICODE. I don't even think this 
			is used in this class anymore. """ 
		unicode_string = unicode_string.encode("ascii", "ignore")
		return unicode_string


def make_paper_objects(dict_of_lists):
	"""takes in dict of info, returns dictionary paper objects like
		["paper_id#"]: paper object """

	id_list = dict_of_lists["id_list"]
	title_list = dict_of_lists["title_list"]
	abstract_list = dict_of_lists["abstract_list"]

	paper_dict = {}
	for i, paper_id in enumerate(id_list):
		paper = Paper()
		paper.id = id_list[i]
		paper.title = title_list[i]
		paper.abstract = abstract_list[i]
		paper_dict[paper_id] = paper

	return paper_dict

		
def get_list_of_all_sentences(paper_dict, q1, q2):
	""" populates paper class properties
	# extracts list of all coocurring sentences """
	list_of_sentences = []
	for key in iter(paper_dict):
		paper_dict[key].split_abstract_into_sentences(q1,q2)
		sentence_list = paper_dict[key].make_sentence_id_tuples()
		list_of_sentences.extend(sentence_list)
		paper_dict[key].word_tokenize()

	return list_of_sentences


def main():
	q1 = "DAT"
	q2 = "ADHD"
	max_num_sents_to_analyze = 23
	
	# retreives info from pubmed
	dict_of_info = get_info_from_xml.main(q1, q2)
	# puts papers into objects
	paper_dict = make_paper_objects(dict_of_info)
	# makes list of all coocurring sentences
	list_of_sentences = get_list_of_all_sentences(paper_dict, q1, q2)
	# ranks sentences and takes top x # (last parameter)
	scored_sentences = rank_sentences.rank_sentences(list_of_sentences, q1,q2, 
													 max_num_sents_to_analyze)
	# THIS IS A BIG DEAL YOU GUYS
	decide_classification.main(scored_sentences, q1, q2)



main()


