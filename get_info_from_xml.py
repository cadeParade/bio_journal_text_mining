import pyquery
import shlex


def get_xml(url):
	xml = pyquery.PyQuery(url)
	return xml

def make_search_url(base_url, q1, q2):
	max_papers = "&retmax=30"
	title_abstract_add = "[tiab]"
	search_url_add = "esearch.fcgi?db=pubmed&term=%s[tiab]+AND+%s[tiab]" %(q1,q2)
	url = base_url+search_url_add + max_papers
	print url
	return url

def make_string_of_ids(xml):
	ids = xml("Id").text()
	ids = ",".join(shlex.split(ids))
	return ids

def make_fetch_url(base_url, fetch_get_abstracts_add, id_string ):
	max_papers = "&retmax=30"
	fetch_url_add = "efetch.fcgi?db=pubmed&id=%s" % id_string
	full_url = base_url + fetch_url_add + fetch_get_abstracts_add + max_papers
	print full_url
	return full_url

def get_info_from_fetch_xml(xml):
	journal_articles = list(xml("PubmedArticle"))
	book_articles = list(xml("PubmedBookArticle"))

	id_list = []
	title_list = []
	abstract_list = []
	
	for doc in journal_articles:
		doc = pyquery.PyQuery(doc)
		doc_list = doc.find("articleid")
		for i in doc_list:
			if i.attrib["idtype"] == "pubmed":
				id_list.append(i.text)
		title_list.append(doc("ArticleTitle").text())
		abstract_list.append(doc("AbstractText").text())

	for doc in book_articles:
		doc = pyquery.PyQuery(doc)
		doc_list = doc.find("articleid")
		for i in doc_list:
			if i.attrib["idtype"] == "pubmed":
				id_list.append(i.text)	
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
	dict_of_info = get_info_from_fetch_xml(docs_xml)
	#paper_dict = make_paper_objects(dict_of_info)

	return dict_of_info


def main(q1, q2):
	paper_dict = get_relevant_data(q1, q2)
	return paper_dict


