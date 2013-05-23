bio journal text mining
=======================

Final project for Hackbright. Mining meaning and correlations out of journal paper abstracts.
Based on this paper: http://www.biomedcentral.com/content/pdf/1471-2105-5-147.pdf  
  
For a high level overview of how it works and to test it, it's hosted [here](http://text_mining.cadeparadeescapades.com).

For a slightly more in depth definition of interesting parts of the program, see below.


## Interesting file descriptions  


**decide_classification.py**    
Here is the meat of the program, in which it figures out whether the terms are interactive or not, based on the structure of the sentence and where the queries are related to other entities. Each sentence that makes it to this function (the 20 with the top score from the ranking) is parsed with the pfp statistical parser and then made into an NLTK tree object (make_tree function, line 46). A depth first search is conducted on each tree, appending to a list each time the search comes across a search term or synonym, a new clause marker, or a verb phrase (traverse function, line 72).  

From here it is easy to find whether the queries are in different clauses (implying non-interaction) and whether the queries are in the same clause and separated by a verb phrase (implying interaction) (find_the_things function, line 116)   

The rest of the file's functions are testing for the presence of telling words (test_for_presence_of_words function, line 145), and a decision tree (decision_time function, line 178) assigning classifications. The overall classification of the interaction is the type that has the most sentences with that classification (decide_overall_classification function, line 207).


**rank_sentences.py**  
Takes list of abstract sentences with both queries in them and ranks them according to points assigned for:  
- short length  
- presence of conclusive words  
- absence of negative words (like "not" or "lack")
- sentences starting with query term or synonym followed directly by a verb  
- presence of query term instead of synonyms
Returns top 20 sentences form this scoring to continue to the parsing in decide_classifications.py
  
  
  

## Other core file descriptions

**server.py**  
Contains all the functions that control the views. Pulls together all the previous files


**do_something_with_the_database.py**  
Contains all functions that interact with the database


**get_info_from_xml.py**  
Contains functions that retrieve abstracts from PubMed and parses the resulting XML into paper objects


**main.py**  
Takes list of paper objects and extracts id, title, authors, abstract, and abstract sentences with both queries into a dictionary.


**papersdb.py**  
Contains model for PostgresSQL database


**query_class_def.py**  
Contains class definition for the query object.


## Peripheral file descriptions:  

**corpus_or_database directory**  
Contains synonym database text file  
 

**static directory**  
Contains html templates, javascript, images, and css  


**word_lists directory**  
Contains lists of important words that are tested for in sentences  


**make_list_of_words.py**  
Makes text files from word_lists directory and puts them in a list.  


**make_syn_dict.py**  
Takes text database in corpus_or_database and converts it into a python dictionary.


