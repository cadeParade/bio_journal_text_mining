import pyquery
import shlex
import do_something_with_the_database

def get_xml(url):
	if url:
		xml = pyquery.PyQuery(url)
		return xml

def make_search_url(base_url, query, max_num_articles_to_get):
	print query.q1_search_string
	print query.q2_search_string
	max_papers = "&retmax=%d" % max_num_articles_to_get
	title_abstract_add = "[tiab]"
	search_url_add = "esearch.fcgi?db=pubmed&term=(%s)+AND+(%s)" %(query.q1, 
																   query.q2)
	url = base_url+search_url_add + max_papers
	print url
	return url

def make_list_of_ids(xml):
	ids = xml("Id").text().split()
	#check if ids are in database
	existing_papers = []
	papers_to_fetch = []
	for _id in ids:
		print _id
		if do_something_with_the_database.paper_exists(_id): 
			existing_papers.append(_id)
			print existing_papers, "EXISTING"
		else:
			papers_to_fetch.append(_id)
			print papers_to_fetch, "GET IT"

	# ids = ",".join(shlex.split(papers_to_fetch))
	stored_and_not_stored_ids = {"existing_papers":existing_papers, 
									"papers_to_fetch":papers_to_fetch}

	return stored_and_not_stored_ids

def make_fetch_url(base_url, fetch_get_abstracts_add, ids, max_num_articles_to_get):
	if ids["papers_to_fetch"]:
		max_papers = "&retmax=%d" % max_num_articles_to_get
		fetch_id_string = ",".join(ids["papers_to_fetch"])
		fetch_url_add = "efetch.fcgi?db=pubmed&id=%s" % fetch_id_string
		full_url = base_url + fetch_url_add + fetch_get_abstracts_add + max_papers
		print full_url
		return full_url
	else:
		return None

def get_info_from_fetch_xml(xml, ids):
	journal_articles = list(xml("PubmedArticle"))
	book_articles = list(xml("PubmedBookArticle"))

	id_list = []
	title_list = []
	abstract_list = []
	authors_list = []

	for doc in journal_articles:
		doc = pyquery.PyQuery(doc)
		doc_list = doc.find("articleid")
		for i in doc_list:
			if i.attrib["idtype"] == "pubmed":
				id_list.append(i.text)
				# print i.text
		authors = doc.find("Author")
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

	return_dict = {"fetched_id_list" : id_list, "title_list":title_list, "abstract_list":abstract_list, "authors_list": authors_list}
	return return_dict

def get_relevant_data(query, max_num_articles_to_get):

	base_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
	#search_url_add = "esearch.fcgi?db=<database>&term=<query>"
	fetch_get_abstracts_add = "&rettype=abstract"
	#url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=science[journal]+AND+breast+cancer+AND+2012[pdat]"

	search_url = make_search_url(base_url, query, max_num_articles_to_get)
	print search_url
	#default return length is 20 docs
	id_xml = get_xml(search_url)
	stored_and_not_stored_ids = make_list_of_ids(id_xml)

	fetched_dict_of_info = {}
	if stored_and_not_stored_ids["papers_to_fetch"]:
		# print stored_and_not_stored_ids
		fetch_url = make_fetch_url(base_url, fetch_get_abstracts_add, stored_and_not_stored_ids, max_num_articles_to_get)
		docs_xml = get_xml(fetch_url)
	
		fetched_dict_of_info = get_info_from_fetch_xml(docs_xml, stored_and_not_stored_ids)
	#paper_dict = make_paper_objects(dict_of_info)

	if fetched_dict_of_info:
		return_dict = {"fetched_dict_of_info":fetched_dict_of_info, "existing_id_list": stored_and_not_stored_ids["existing_papers"]}
		return return_dict
	else:
		return_dict = {"existing_id_list":stored_and_not_stored_ids["existing_papers"]}
		return return_dict


def main(query, max_num_articles_to_get):
	fetched_dict_of_info = get_relevant_data(query, max_num_articles_to_get)
	return fetched_dict_of_info


