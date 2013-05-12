import pyquery
import shlex

base_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
search_url_add = "esearch.fcgi?db=<database>&term=<query>"
fetch_get_abstracts_add = "&rettype=abstract"
# url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=science[journal]+AND+breast+cancer+AND+2012[pdat]"

url =  "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=23597510,23595734,23585124,23574441,23571119,23542690,23518710,23494234,23481387,23475113&rettype=abstract&retmax=10"


def get_xml(url):
	f = pyquery.PyQuery(url)
	return f


def get_info_from_fetch_xml(xml):
	journal_articles = list(xml("PubmedArticle"))
	book_articles = list(xml("PubmedBookArticle"))
		
	
	id_list = []
	title_list = []
	abstract_list = []
	authors_list = []
	mesh_terms_list = []
	
	for doc in journal_articles:
		doc = pyquery.PyQuery(doc)
		doc_list = doc.find("articleid")
		for i in doc_list:
			if i.attrib["idtype"] == "pubmed":
				id_list.append(i.text)
				# print i.text
		title_list.append(doc("ArticleTitle").text())
		abstract_list.append(doc("AbstractText").text())
		authors_list.append(doc("AuthorList").text())

	for doc in book_articles:
		doc = pyquery.PyQuery(doc)
		doc_list = doc.find("articleid")
		for i in doc_list:
			if i.attrib["idtype"] == "pubmed":
				id_list.append(i.text)	
		title_list.append(doc("ArticleTitle").text())
		abstract_list.append(doc("AbstractText").text())
		authors_list.append(doc("AuthorList").text())


	print len(abstract_list), "length of abstract list"
	print authors_list
	

	return_dict = {"id_list" : id_list, "title_list":title_list, "abstract_list":abstract_list}
	return return_dict
	
	
id_xml = get_xml(url)
get_info_from_fetch_xml(id_xml)