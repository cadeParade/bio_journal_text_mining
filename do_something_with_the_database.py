from flask import Flask, render_template, redirect, request, flash, url_for, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Date, types, asc
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

import papersdb
import datetime

# database columns
# class Paper(Base):
#     id = Column(Integer, primary_key = True)
#     pubmed_id = Column(String(16))
#     title = Column(Text)
#     authors = Column(Text)

# class Sentences(Base):
#     id = Column(Integer, primary_key = True)
#     paper_id = Column(Integer)
#     sentence = Column(Text)
#     sentence_order = Column(Integer)
#     parsed_sentence = Column(Text)

def paper_exists(pubmed_id):
	paper_exists = papersdb.session.query(papersdb.Paper).filter_by(pubmed_id=pubmed_id).first()
	if paper_exists:
		#check if parsed sentences exist
		return True
	else:
		return False

def get_paper_info(pubmed_id):
	paper_info_dict = {}
	current_paper = papersdb.session.query(papersdb.Paper).filter_by(pubmed_id = pubmed_id).first()
	return current_paper


def assemble_abstract(pubmed_id):
	current_abstract = papersdb.session.query(papersdb.Sentences).filter_by(paper_id =pubmed_id) \
																 .order_by(asc(papersdb.Sentences.sentence_order)) \
																 .all()
	#returns list of db objects
	return current_abstract


def check_for_tree(sentence):
	tree_exists = papersdb.session.query(papersdb.Sentences).filter_by(sentence=sentence).first()
	if tree_exists:
		return True
	else:
		return False

def get_tree(sentence):
	sent = papersdb.session.query(papersdb.Sentences).filter_by(sentence = sentence).first()
	tree = sent.parsed_sentence
	return tree 

def sent_tree_exists(sentence_paper_id, sentence_order):
	sentences_in_abstract = papersdb.session.query(papersdb.Sentences).filter_by(paper_id=sentence_paper_id).all()
	import pdb; pdb.set_trace();
	for sentence in sentences_in_abstract:
		if sentence.parsed_sentence:
			pass
		

def add_new_paper(paper_dict):
	for key, paper in paper_dict.iteritems():	
		if paper_exists(paper.id) == False:
			
			#adds new paper to paper db
			new_paper = papersdb.Paper(pubmed_id=paper.id, 
									   title = paper.title, 
									   authors = paper.authors)
			papersdb.session.add(new_paper)

			# makes empty list length of all sentences
			# is populated with parsed sentence trees at the indexes of sentences they
			# first appeared at (so if the 3rd sentence is parsed it will show in the 
			# list as index 2)
			tree_list = [None]*len(paper.all_sentences)
			#populates list only at indexes where trees exist
			if paper.classified_sentences:
				for local_sentence in paper.classified_sentences:
					tree_list[local_sentence.order_in_abstract] = local_sentence.tree._pprint_flat(nodesep='', parens='()', quotes=False)

			
			for i, sentence in enumerate(paper.all_sentences):

				new_sentence = papersdb.Sentences(paper_id = paper.id,
												  sentence = sentence,
												  sentence_order = i,
												  parsed_sentence = tree_list[i])
				papersdb.session.add(new_sentence)


	papersdb.session.commit()











