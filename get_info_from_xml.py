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
	search_url_add = "esearch.fcgi?db=pubmed&term=(%s)+AND+(%s)" %(query.q1_search_string, 
																   query.q2_search_string)
	url = base_url+search_url_add + max_papers
	print url
	return url

def make_list_of_ids(xml):
	#
	#
	#
	#
	#
	#
	#
	##### IF NO INTERNET ############
	######## FOR TLR3 + TLR4 ################
	# stored_and_not_stored_ids = {"existing_papers":['23644550', '23628388', '23610145', '23593278', '23587629', '23552014', '23545497', '23532979', '23509365', '23509149', '23489833', '23480796', '23469297', '23429540', '23417039', '23407750', '23375594', '23374856', '23365087', '23352460', '23350674', '23348232', '23345580', '23342077', '23341538', '23314616', '23296707', '23287555', '23284890', '23278752', '23266719', '23238454', '23212905', '23209321', '23207548', '23206318', '23192653', '23179584', '23166161', '23159604', '23159338', '23151845', '23151015', '23146386', '23142523', '23142133', '23132491', '23116495', '23086657', '23062198', '23030425', '23028330', '23026026', '23023072', '23016675', '23013528', '23002119', '22994343', '22994237', '22986631', '22986167', '22984265', '22923219', '22916277', '22915814', '22842032', '22809727', '22808176', '22754655', '22753953', '22751696', '22732735', '22727330', '22726246', '22709825', '22699880', '22690903', '22689135', '22637968', '22635047', '22634618', '22627090', '22622619', '22579417', '22578853', '22562536', '22546503', '22542815', '22499581', '22497726', '22491257', '22479513', '22466124', '22388837', '22442690', '22440523', '22429150', '22427633', '22355412', '22344343'], 
	# 								"papers_to_fetch":[]}
	######## FOR DAT-1 AND ADHD
	# stored_and_not_stored_ids = {"existing_papers":['23623751', '23555781', '23541676', '23447367', '23397052', '23303075', '23273726', '23255304', '23197772', '23192105', '23026058', '22816024', '22796428', '22580232', '22561003', '22514303', '22470460', '22298359', '22133315', '22119644', '22034972', '22024001', '21956611', '21778150', '21716015', '21559387', '21516392', '21497794', '21439946', '21432601', '21432587', '21207367', '21150910', '20957668', '20720111', '20641907', '20593420', '20493667', '20415606', '20211696', '20049490', '19854053', '19767592', '19738093', '19699754', '19670315', '19388000', '19364291', '19176281', '19128199', '18824036', '18802919', '18772050', '18614672', '18580852', '18563476', '18416663', '18304369', '18282769', '18188752', '18081165', '18057916', '17980763', '17671965', '17555897', '17511972', '17464676', '17440978', '17433376', '17375139', '17318414', '17316796', '17275916', '17255472', '17227286', '17201613', '17197367', '17187001', '17171650', '17073682', '17063150', '17044101', '17017960', '16961425', '16922923', '16894328', '16861140', '16774975', '16756025', '16722244', '16678430', '16647218', '16640111', '16613553', '16555214', '16490314', '16451810', '16402340', '16309561', '16261167'],
	# 							 "papers_to_fetch":[]}
	# return stored_and_not_stored_ids
	#
	###### FOR INSULIN AND DIABETES ###############
	# stored_and_not_stored_ids = {"existing_papers":['23641356', '23641355', '23641352', '23641235', '23641007', '23640967', '23640946', '23640936', '23640882', '23640708', '23640454', '23640247', '23640034', '23639858', '23639840', '23639570', '23639568', '23639525', '23638994', '23638642', '23638607', '23638493', '23638297', '23637966', '23637851', '23637777', '23637538', '23637357', '23637348', '23637016', '23636998', '23636657', '23636640', '23636445', '23636267', '23635650', '23635500', '23635430', '23635406', '23635096', '23634804', '23634778', '23634670', '23631572', '23627322', '23633768', '23633679', '23633532', '23633415', '23633364', '23633267', '23633201', '23633196', '23633194', '23633155', '23632905', '23632402', '23632200', '23632173', '23632126', '23631851', '23631624', '23631608', '23631607', '23631604', '23631497', '23631462', '23631252', '23631205', '23631191', '23630454', '23630453', '23630416', '23630302', '23630301', '23630299'],
	# 							 "papers_to_fetch":[]}
	# return stored_and_not_stored_ids
	#
	#
	#
	#
	#

	########### IF NO INTERNET COMMENT OUT REST OF FUNCTION #################
	ids = xml("Id").text().split()
	#check if ids are in database
	existing_papers = []
	papers_to_fetch = []
	for _id in ids:
		if do_something_with_the_database.paper_exists(_id): 
			existing_papers.append(_id)
		else:
			papers_to_fetch.append(_id)

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
		max_papers = "&retmax=%d" % max_num_articles_to_get
		fetch_id_string = ",".join(ids["papers_to_fetch"])
		fetch_url_add = "efetch.fcgi?db=pubmed&id=%s" % fetch_id_string
		full_url = base_url + fetch_url_add + fetch_get_abstracts_add + max_papers
		print full_url
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

	search_url = make_search_url(base_url, 
							     query, 
							     max_num_articles_to_get)
	print search_url
	#default return length is 20 docs
	
	#
	#
	#
	#
	#
	#
	#

	########## IF NO INTERNET, COMMENT OUT BELOW LINE 
	id_xml = get_xml(search_url)

	######### IF NO INTERNET, COMMENT IN LINE BELOW
	# id_xml = ""
	#
	#
	#
	#
	#
	#

	stored_and_not_stored_ids = make_list_of_ids(id_xml)

	fetched_dict_of_info = {}
	if stored_and_not_stored_ids["papers_to_fetch"]:
		fetch_url = make_fetch_url(base_url, 
			                       fetch_get_abstracts_add, 
			                       stored_and_not_stored_ids, 
			                       max_num_articles_to_get)
		docs_xml = get_xml(fetch_url)
	
		fetched_dict_of_info = get_info_from_fetch_xml(docs_xml, 
													   stored_and_not_stored_ids)
	#paper_dict = make_paper_objects(dict_of_info)

	if fetched_dict_of_info:
		return_dict = {"fetched_dict_of_info":fetched_dict_of_info, 
					   "existing_id_list": stored_and_not_stored_ids["existing_papers"]}
		return return_dict
	else:
		return_dict = {"existing_id_list":stored_and_not_stored_ids["existing_papers"]}
		return return_dict


def main(query, max_num_articles_to_get):
	fetched_dict_of_info = get_relevant_data(query, max_num_articles_to_get)
	return fetched_dict_of_info


