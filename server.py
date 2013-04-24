from flask import Flask, render_template, request, redirect, make_response 
from jinja2 import Template
import main


app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/search_output", methods = ["POST"])
def search_output():
	q1 = request.form["q1"]
	q2 = request.form["q2"]
	scored_sentences = []
	
	scored_sentence_tuples = main.main(q1, q2)
	
	
	for sentence in scored_sentence_tuples:
		scored_sentences.append(sentence[2])

	return render_template("search_output.html", q1 = q1, q2 = q2, scored_sentences = scored_sentences)

	
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