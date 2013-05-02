from flask import Flask, render_template, request, redirect, make_response 
from jinja2 import Template
import main
import query_class_def
import get_info_from_xml
import rank_sentences
import decide_classification
import pusher
import papersdb
import do_something_with_the_database

# p = pusher.Pusher(app_id='42611', key='9289758c45b094b1f969', secret='fb86f119bee7300dcf48')
# p['my-channel'].trigger('my-event',{'message': 'hello world'})


app = Flask(__name__)

def format_display_items(paper_dict):
	papers_with_relevant_sentences = []
	
	for key in paper_dict.iterkeys():
		if paper_dict[key].classified_sentences:
			papers_with_relevant_sentences.append(paper_dict[key])
	
	display_items = []

	for paper in papers_with_relevant_sentences:
		sentence_list = []

		for sentence in paper.classified_sentences:
			sentence_w_classification = (sentence.sentence, 
										 sentence.overall_classification, 
										 sentence.general_classification)
			sentence_list.append(sentence_w_classification)
		item = (paper.id, paper.title, sentence_list)
		display_items.append(item)
	# format of display_items	
	# display_items = [(pubmed_id, "title", [("classified sentence", 
	#										  "overall class", "general class"),
	#										 ("classified sentence", 
	#										  "overall class", "general class")])]
	return display_items


@app.route("/",  methods = ["GET", "POST"])
def index():
	#displays home page
	if request.method == "GET":
		return render_template("index.html")

	#displays search results page
	else:

		max_num_sents_to_analyze = 20
		syn_dict_location = "corpus_or_database/chilibot.syno.database"
		
		q1 = request.form["q1"]
		q2 = request.form["q2"]


		query = query_class_def.main(q1, q2, syn_dict_location)

		#makes dictionary of paper objects
		paper_dict = main.main(query)
		#creates list of all sentences with both query terms
		list_of_sentences = main.get_list_of_all_sentences(paper_dict,query)
		#list of tuples, (score, pubmed_id, sentence text), as many as cutoff number above
		scored_sentences = rank_sentences.rank_sentences(list_of_sentences, 
														 query, 
														 max_num_sents_to_analyze)
		#list of sentences with classification properties filled in
		classified_sentence_list = decide_classification.main(scored_sentences, query)
		# returns dict {"count": #, "text": "classification label"}
		overall_classification = decide_classification.count_papers_of_each_type(classified_sentence_list)
		#assigns classified sentences to paper object that they came from
		main.assign_sentences_back_from_which_they_came(paper_dict, classified_sentence_list)
		#formats things to display in html
		display_items = format_display_items(paper_dict)
		#enters papers into database if they aren't already there
		do_something_with_the_database.add_new_paper(paper_dict)



		return render_template("search_output.html", q1 = q1, q2 = q2, 
													 overall_classification = overall_classification,
													 display_items = display_items)

# @app.route("/",  methods = ["GET", "POST"])
# def index():



if __name__ == "__main__":
	app.run(debug=True)