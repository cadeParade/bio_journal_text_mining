import urllib
import pyquery
import shlex
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.tag import pos_tag
import pfp
import unicodedata



class Abstract(object):

	def __init__(self):
		self.title = None
		self.abstract = None
		self.abstract_sentences = None
		self.sentences_tagged = None


	def split_abstract_into_sentences(self, paper_dict, q1, q2):
		for key in iter(paper_dict):
			if paper_dict[key]["abstract"]:
				current_abstract = paper_dict[key]["abstract"]
				sentence_list = current_abstract.split(".")

				coocurrence = find_sentences_with_both_queries(sentence_list, q1, q2)
				
				paper_dict[key]["coocurrence"] = coocurrence
				print paper_dict[key]["coocurrence"]
			else: 
				paper_dict[key]["coocurrence"] = None
				print "hi"

		return paper_dict



def get_xml(url):
	xml = pyquery.PyQuery(url)
	return xml

def make_search_url(base_url, q1, q2):
	title_abstract_add = "[tiab]"
	search_url_add = "esearch.fcgi?db=pubmed&term=%s+AND+%s" %(q1,q2)
	url = base_url+search_url_add+title_abstract_add
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
	print len(xml)
	single_docs = xml("PubmedArticle")
	print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
	print len(single_docs)
	id_list = id_list.split(",")	
	title_list = []
	abstract_list = []
	for doc in single_docs:
		doc = pyquery.PyQuery(doc)
		title_list.append(doc("ArticleTitle").text())
		abstract_list.append(doc("AbstractText").text())

	return_list = [id_list, title_list, abstract_list]
	return return_list

def make_dict_of_docs(list_of_lists):
	id_list = list_of_lists[0]
	title_list = list_of_lists[1]
	abstract_list = list_of_lists[2]

	paper_dict = {}
	for i, paper in enumerate(id_list):
		paper_dict[paper] = {"id": paper, "title":title_list[i], "abstract":abstract_list[i]}

	return paper_dict


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
	fetch_url = make_fetch_url(base_url, fetch_get_abstracts_add, id_string)
	docs_xml = get_xml(fetch_url)
	list_of_info = get_info_from_fetch_xml(docs_xml, id_string)
	paper_dict = make_dict_of_docs(list_of_info)

	return paper_dict

def split_abstract_into_sentences(paper_dict, q1, q2):
	"""takes in dictionary with abstracts, returns same dictionary with 
		new dict key of sentences containing both queries"""
	for key in iter(paper_dict):
		if paper_dict[key]["abstract"]:
			current_abstract = paper_dict[key]["abstract"]
			#splits paragraphs into sentences with NLTK function
			sentence_list = sent_tokenize(current_abstract)
			coocurrence = find_sentences_with_both_queries(sentence_list, q1, q2)
			
			paper_dict[key]["coocurrence"] = coocurrence
		else: 
			paper_dict[key]["coocurrence"] = None

	return paper_dict

def find_sentences_with_both_queries(sentence_list, q1, q2):
	"""takes list of sentences, tests if both queries are in each 
		sentence. If so, keeps, if not, deletes"""
	coocurrence_list = []
	for sentence in sentence_list:
		if q1 in sentence and q2 in sentence:
			coocurrence_list.append(sentence)
	return coocurrence_list

def word_tokenize(paper_dict):
	tokenizer = RegexpTokenizer("\s+", gaps = True)

	for key in iter(paper_dict):
		if paper_dict[key]["coocurrence"]:
			word_tokenized = []
			for sentence in paper_dict[key]["coocurrence"]:
				tokenized_words =  tokenizer.tokenize(sentence)
				word_tokenized.append(tokenized_words)
		else:
			word_tokenized = None
		paper_dict[key]["word_tokenized"] = word_tokenized
	return paper_dict

def pos_tagger(paper_dict):
	for key in iter(paper_dict):
		if paper_dict[key]["word_tokenized"]:
			for sentence in paper_dict[key]["word_tokenized"]:
				pass

def show(s):
	ps = pfp.Parser().parse(s)
	tree = nltk.ImmutableTree.parse(ps)
	print tree


def main():
	q1 = "ADHD"
	q2 = "DAT"
	paper_dict = get_relevant_data(q1, q2)
	paper_dict_sentence_split = split_abstract_into_sentences(paper_dict, q1, q2)
	paper_dict_word_split = word_tokenize(paper_dict_sentence_split)
	
	pos_tagger(paper_dict_word_split)

	for key in iter(paper_dict_sentence_split):
		for sentence in paper_dict_sentence_split[key]["coocurrence"]:
			print sentence
			if type(sentence) != str:
				sentence = sentence.encode("ascii", "ignore")
			show(sentence)


	




main()
















