def make_list_of_syns(text_file):
	word_list = []
	f = open(text_file)
	for line in f:
		line = line.strip()
		word_list.append(line)
	f.close()
	return word_list