import pfp
import unicodedata
import re
import nltk


q1 = "DAT"
q2 = "ADHD"


string = "Deregulation of DAT function has been linked to several neurological and psychiatric disorders including ADHD, schizophrenia, Parkinson's disease, and drug addiction"
string2 = "10/10 DAT allele seems to be associated with an increased expression level of the dopamine transporter and seems to mediate the MPH treatment response in ADHD patients"
string3 = "Relationship between DAT VNTR genotypes and neurocognitive response to MPH was analyzed in a sample of 108 drug-naive ADHD patients"
string4 = "Neurocognitive effects of methylphenidate on ADHD children with different DAT genotypes: A longitudinal open label trial."
string5 = "Our findings suggest that an ADHD risk polymorphism (3'-UTR) of SLC6A3 has functional consequences on central nervous system DAT binding in humans"

sentences = [string, string2, string3, string4, string5]

if isinstance(string, unicode):
	string = sentence.encode("ascii", "ignore")

parsed_sentence = pfp.Parser().parse(string)
dat_index = parsed_sentence.index(q1)
adhd_index = parsed_sentence.index(q2)


for string in sentences:

	#converts to ascii if unicode
	if isinstance(string, unicode):
		string = string.encode("ascii", "ignore")

	#shallow parsing	
	parsed_sentence = pfp.Parser().parse(string)
	tree = nltk.ImmutableTree.parse(parsed_sentence)
	print tree

	#find query 1
	q1_index = parsed_sentence.index(q1)
	#find query 2
	q2_index = parsed_sentence.index(q2)

	#make list of indexes of where "(VP " appears
	if "(VP " in parsed_sentence:
		vp_index_list = [m.start() for m in re.finditer("\(VP ", parsed_sentence)]
	else:
		vp_index_list = None

	#decides whether "(VP " is between the two queries
	if vp_index_list:
		if q1_index < q2_index:
			is_vp_between_queries =  any(q1_index < index < q2_index for index in vp_index_list)
			# print "q1 is first at %d , vp is at %r, q2 is at %d" %(q1_index, vp_index_list, q2_index)
			# print is_vp_between_queries
			# print "                      "
		elif q2_index < q1_index:
			is_vp_between_queries = any(q2_index < index < q1_index for index in vp_index_list)
			# print "q2 is first at %d , vp is at %r, q1 is at %d" %(q2_index, vp_index_list, q1_index)
			# print is_vp_between_queries
			# print "                      "
		else:
			is_vp_between_queries = False
	else:
		# print "vp is not present"
		is_vp_between_queries = False


		
