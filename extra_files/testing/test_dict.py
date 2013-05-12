raw_dict = open("corpus_or_database/chilibot.syno.database")
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



