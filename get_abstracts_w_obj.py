import pyquery
import shlex
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.tag import pos_tag
import pfp
import unicodedata
import re


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
		self.title = None
		self.abstract = None
		self.all_sentences = None
		self.word_tokenized = None
		self.sentences_tagged = None
		self.coocurring_sentences = None
		self.pos_tagged = None

	def make_sentence_id_tuples(self):
		list_of_tuples = []
		for sentence in self.coocurring_sentences:
			current_tuple = (self.id, sentence, 0)
			list_of_tuples.append(current_tuple)
		# print self.coocurring_sentences
		# print list_of_tuples
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
			sentence. If so, keeps, if not, deletes"""
		coocurrence_list = []
		for sentence in sentence_list:
			if q1 in sentence and q2 in sentence:
				coocurrence_list.append(sentence)
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

	def pos_tagger(self):
		""" part of speech tagger for sentences split into a list of words """
		if self.word_tokenized:
			self.pos_tagged = []
			for sentence in self.word_tokenized:
				self.pos_tagged.append(nltk.pos_tag(sentence))

	def convert_unicode_to_ascii(self,unicode_string):
		unicode_string = unicode_string.encode("ascii", "ignore")
		return unicode_string

	def shallow_parsing(self):
		""" takes sentences and identifies noun and verb phrases """
		for i,sentence in enumerate(self.coocurring_sentences):
			if self.coocurring_sentences:
				if isinstance(sentence, unicode):
					sentence = self.convert_unicode_to_ascii(sentence)

				parsed_sentence = pfp.Parser().parse(sentence)
				#tree = nltk.ImmutableTree.parse(parsed_sentence)


#################### get info from pubmed ##############

def get_xml(url):
	xml = pyquery.PyQuery(url)
	return xml

def make_search_url(base_url, q1, q2):
	max_papers = "&retmax=20"
	title_abstract_add = "[tiab]"
	search_url_add = "esearch.fcgi?db=pubmed&term=%s+AND+%s" %(q1,q2)
	url = base_url+search_url_add+title_abstract_add + max_papers
	print url
	return url

def make_string_of_ids(xml):
	ids = xml("Id").text()
	ids = ids = ",".join(shlex.split(ids))
	return ids

def make_fetch_url(base_url, fetch_get_abstracts_add, id_string ):
	fetch_url_add = "efetch.fcgi?db=pubmed&id=%s" % id_string
	full_url = base_url + fetch_url_add + fetch_get_abstracts_add
	return full_url

def get_info_from_fetch_xml(xml, id_list):
	print len(xml), "length of xml"
	single_docs = xml("PubmedArticle")
	print len(single_docs), "length of list of articles"
	id_list = id_list.split(",")	
	title_list = []
	abstract_list = []
	for doc in single_docs:
		doc = pyquery.PyQuery(doc)
		title_list.append(doc("ArticleTitle").text())
		abstract_list.append(doc("AbstractText").text())
	print len(abstract_list), "length of abstract list"

	return_dict = {"id_list" : id_list, "title_list":title_list, "abstract_list":abstract_list}
	return return_dict

def get_relevant_data(q1,q2):

	base_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
	#search_url_add = "esearch.fcgi?db=<database>&term=<query>"
	fetch_get_abstracts_add = "&rettype=abstract"
	#url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=science[journal]+AND+breast+cancer+AND+2012[pdat]"

	search_url = make_search_url(base_url,q1,q2)
	print search_url
	#default return length is 20 docs
	id_xml = get_xml(search_url)
	id_string = make_string_of_ids(id_xml)
	print id_string
	fetch_url = make_fetch_url(base_url, fetch_get_abstracts_add, id_string)
	docs_xml = get_xml(fetch_url)
	dict_of_info = get_info_from_fetch_xml(docs_xml, id_string)
	paper_dict = make_paper_objects(dict_of_info)

	return paper_dict

#########################################################

def make_paper_objects(dict_of_lists):
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


def make_list_of_all_sentences():
	pass
	

def main():
	q1 = "DAT"
	q2 = "ADHD"
	paper_dict = get_relevant_data(q1, q2)
	list_of_sentences = []
	for key in iter(paper_dict):
		paper_dict[key].split_abstract_into_sentences(q1,q2)
		sentence_list = paper_dict[key].make_sentence_id_tuples()
		list_of_sentences.extend(sentence_list)
		paper_dict[key].word_tokenize()
		#paper_dict[key].pos_tagger()
		#paper_dict[key].shallow_parsing()
	

	for sentence_tuple in list_of_sentences:
		sentence = sentence_tuple[1]
		sentence_words = sentence.split()
		print sentence_words
		score = 0



		# PRESENCE OF SUGGEST, FOUND, SHOW, DATA
		good_words = ["suggest", "found", "show", "data"]
		if any(word in sentence for word in good_words):
			score += 9

		#SENTENCE LENGTH
		sentence_length = len(re.findall(r'\w+', sentence))
		if sentence_length > 30:
			score -= 3

	 	
		#do the ranking 
		#if there's a value
		#for each tuple in the list ("id", "sentence", 'score')
			# score = 0
			#current sentence = current_tuple[1]
			#processing on current sentence
			# various things happen += score


	




main()
















