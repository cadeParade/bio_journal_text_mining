import pfp
import nltk

""" takes in a list of sentences
	returns sentences with classification """


def shallow_parsing(sentence):
		""" takes sentences and identifies noun and verb phrases """
		if isinstance(sentence, unicode):
			sentence = sentence.encode("ascii", "ignore")

		parsed_sentence = pfp.Parser().parse(sentence)
		# tree = nltk.ImmutableTree.parse(parsed_sentence)
		# print tree
		return parsed_sentence

def parse_sentences(scored_sentences):
	""" parses top x sentences
		which are in format (ranking, id of paper it came from, sentence)
		and identifies whether VP in between search terms """
	parsed_sentences = []
	for sentence in scored_sentences:
		parsed_sentence = shallow_parsing(sentence[2])
		parsed_sentences.append(parsed_sentence)
	return parsed_sentences



def main(scored_sentences):
	print scored_sentences
	parse_sentences(scored_sentences)
	
		