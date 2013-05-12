from flask import Flask, render_template, request, redirect, make_response 
from jinja2 import Template
import main
import pusher

p = pusher.Pusher(app_id='42611', key='9289758c45b094b1f969', secret='fb86f119bee7300dcf48')
p['my-channel'].trigger('my-event',{'message': 'hello world'})

display_items = [('23555781', u'Inhibition of Dopamine Transporter Activity by G Protein \u03b2\u03b3 Subunits.', [" Deregulation of DAT function has been linked to several neurological and psychiatric disorders including ADHD, schizophrenia, Parkinson's disease, and drug addiction"]), ('23397052', 'Impaired cliff avoidance reaction in dopamine transporter knockout mice.', [' Dopamine transporter knockout (DAT-KO) mice display features of ADHD and are candidates in which to test other impulsive phenotypes']), ('23192105', 'Immunization with DAT fragments is associated with long-term striatal impairment, hyperactivity and reduced cognitive flexibility in mice.', [' Levels of brain dopamine transporter (DAT) have been implicated in several impulse-control disorders, like attention deficit / hyperactivity disorder (ADHD) and obsessive-compulsive disorder (OCD)']), ('23255304', 'Association of dopamine transporter gene variants with childhood ADHD features in bipolar disorder.', ['3 near the dopamine transporter gene (DAT1), which has been associated with both BD and ADHD']), ('23273726', 'Functional Genomics of Attention-Deficit/Hyperactivity Disorder (ADHD) Risk Alleles on Dopamine Transporter Binding in ADHD and Healthy Control Subjects.', [" Our findings suggest that an ADHD risk polymorphism (3'-UTR) of SLC6A3 has functional consequences on central nervous system DAT binding in humans", " Both ADHD status and the 3'-UTR polymorphism status had an additive effect on DAT binding", " CONCLUSIONS: The 3'-UTR but not intron8 VNTR genotypes were associated with increased DAT binding in both ADHD patients and healthy control subjects"]), ('23541676', 'Neurocognitive effects of methylphenidate on ADHD children with different DAT genotypes: A longitudinal open label trial.', [' 10/10 DAT allele seems to be associated with an increased expression level of the dopamine transporter and seems to mediate the MPH treatment response in ADHD patients', 'Neurocognitive effects of methylphenidate on ADHD children with different DAT genotypes: A longitudinal open label trial.', ' Relationship between DAT VNTR genotypes and neurocognitive response to MPH was analyzed in a sample of 108 drug-naive ADHD patients']), ('23197772', 'In vivo occupancy of dopamine D3 receptors by antagonists produces neurochemical and behavioral effects of potential relevance to attention-deficit-hyperactivity disorder.', [' Mice in which the dopamine transporter (DAT) has been deleted exhibit hyperactivity that is normalized by compounds that are effective in the treatment of ADHD'])]


app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index_test.html")

@app.route("/search_output", methods = ["POST"])
def search_output():
	q1 = request.form["q1"]
	q2 = request.form["q2"]
	classified_sentences = []
	
	#papers_with_relevant_sentences = main.main(q1, q2)

	# display_items = []

	# for paper in papers_with_relevant_sentences:
	# 	sentence_list = []
	# 	for sentence in paper.classified_sentences:
	# 		sentence_list.append(sentence.sentence)
	# 	item = (paper.id, paper.title, sentence_list)
	# 	display_items.append(item)

	

	return render_template("search_output_test.html", q1 = q1, q2 = q2, 
												 display_items = display_items)

	
# @app.route("/output_table", methods = ["POST"])
# def make_output_page():
# 	b1 = request.form["b1"]
# 	b2 = request.form["b2"]
# 	gene_name = request.form["gene_name"]
# 	wt = request.form["wt"]
# 	sequences = request.form["sequences"]

# 	sequence_list = indel_finder_web.find_indels(b1,b2,gene_name, wt, sequences)
# 	table_html = indel_finder_web.outputs_html(sequence_list, wt)

# 	return render_template("table_template.html", 
# 						   gene_name = gene_name, data = table_html,
# 						   b1 = b1, b2 = b2, wt = wt, sequences = sequences)

# @app.route("/csv", methods = ["POST"])
# def make_csv_file():
# 	b1 = request.form["b1"]
# 	b2 = request.form["b2"]
# 	gene_name = request.form["gene_name"]
# 	wt = request.form["wt"]
# 	sequences = request.form["sequences"]

# 	sequence_list = indel_finder_web.find_indels(b1, b2, gene_name, wt, sequences)
# 	csv = indel_finder_web.make_csv(sequence_list)
# 	csv_file = open("summary.csv", "rb")
# 	csv_read = csv_file.read()

# 	response = make_response(csv_read)
# 	response.headers['Content-Disposition'] = "attachment; filename=\"summary_" + gene_name + ".csv\""
# 	return response



# @app.route("/fasta", methods = ["POST"])
# def make_fasta_file():
# 	b1 = request.form["b1"]
# 	b2 = request.form["b2"]
# 	gene_name = request.form["gene_name"]
# 	wt = request.form["wt"]
# 	sequences = request.form["sequences"]

# 	sequence_list = indel_finder_web.find_indels(b1, b2, gene_name, wt, sequences)
# 	output_list = indel_finder_web.make_output_list(sequence_list)
# 	wt = indel_finder_web.make_string_seqrecord(indel_finder_web.sanitize_wt(wt), "wt")
# 	fasta = indel_finder_web.write_fasta(output_list, wt)

# 	# #### GET FILE NAME OUT??!?!?!?!###############

# 	opened_fasta = open("align.seq", "rU")
# 	fasta_lines_list = opened_fasta.readlines()

# 	return "<br>".join(fasta_lines_list)
	


if __name__ == "__main__":
	app.run(debug=True)