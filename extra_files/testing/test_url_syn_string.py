def make_syn_dict(filename = "corpus_or_database/chilibot.syno.database"):
	
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


syn_dict = make_syn_dict()

print syn_dict["DAT"]
syn_list = syn_dict["DAT"]
string = ""

for i, syn in enumerate(syn_list):

	if i < len(syn_list) - 2:
		string += syn+"[tiab]+OR+"
	else:
		string += syn

print string