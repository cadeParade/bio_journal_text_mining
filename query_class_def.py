
class Query(object):

	def __init__(self):
		self.q1 = None
		self.q1_syns = None		
		
		self.q2 = None
		self.q2_syns = None

		syn_dict = None

	# def get_syns(self, q):
	# 	syn_list = None
	# 	if q in self.syn_dict:
	# 		syn_list = syn_dict[q]
		
	# 	return syn_list	

	# def make_list_of_all_sentences(self):
	# 	pass

	# def pair_sentences_with_paper_id(self):
	# 	pass

	def make_syn_dict(self, filename):
		
		raw_dict = open(filename)
		syn_dict = {}

		for line in raw_dict:
			term_and_syns = line.split("|")
			key = term_and_syns[0]
			values = term_and_syns[1]

			#cleaning up values string
			values = values.strip("\n")
			if values[-1] == ";":
				values = values[0:-2]

			value_list = values.split(";")

			syn_dict[key] = value_list

		return syn_dict

	def get_syns(self, q):
		syn_list = None
		if q in self.syn_dict:
			syn_list = self.syn_dict[q]
		
		return syn_list	





def make_query_object(q1, q2, syn_dict_location):
	query = Query()
	query.syn_dict = query.make_syn_dict(syn_dict_location)
	query.q1 = q1
	query.q2 = q2
	query.q1_syns = query.get_syns(query.q1)
	query.q2_syns = query.get_syns(query.q2)

	return query




def main(q1, q2, syn_dict_location):
	#syn_dict_location = "corpus_or_database/chilibot.syno.database"
	#syn_dict = make_syn_dict(syn_dict_location)

	queries = make_query_object(q1, q2, syn_dict_location)

	print queries.q1
	print queries.q2
	print queries.q1_syns


	
