import nltk
import pfp
import re


sentence = "Dopamine transporter knockout (DAT-KO) mice display features of ADHD and are candidates in which to test other impulsive phenotypes"
sentence2 = "10/10 DAT allele seems to be associated with an increased expression level of the dopamine transporter and seems to mediate the MPH treatment response in ADHD patients"
sentence3 = "The ADHD status was associated with increased striatal (caudate) DAT binding regardless of 3'-UTR genotype, and 3'-UTR genotype was associated with increased striatal (caudate) DAT binding regardless of ADHD status"
sentence4 = "Both ADHD status and the 3'-UTR polymorphism status had an additive effect on DAT binding 3'-UTR near the dopamine transporter gene (DAT1), which has been associated with both BD and ADHD"
sentence5 = "Mice in which the dopamine transporter (DAT) has been deleted exhibit hyperactivity that is normalized by compounds that are effective in the treatment of ADHD"
sentence6 = "DAT-CI mice are hyperdopaminergic due to reduced DAT function, and may thus be a good model for studying attention deficit hyperactivity disorder (ADHD)"
sentence7 = "Together, our studies support a coupling of DAT microdomain localization with transporter regulation and provide evidence of perturbed DAT activity and DA signaling as a risk determinant for ADHD"
sentence8 = "The presynaptic, cocaine- and amphetamine (AMPH)-sensitive DA transporter (DAT) constrains DA availability at presynaptic and postsynaptic receptors following vesicular release and is targeted by the most commonly prescribed ADHD therapeutics"
sentence9 = "Ritalin(\xae) (methylphenidate, MPH), a DAT-blocking drug, is prescribed for ADHD therapy but is also widely abused by human adolescents"

#sentence 1 = worked
#sentence 2 = unclear (queries ARE in different clauses, but interaction still implied)
#sentence 3 = worked
#sentence 4 = unclear (parsing is strange)
#sentence 5 = unclear (queries ARE in different clauses, but interaction is still implied)
#sentence 6 = only one s between clauses


sentence_list = [sentence, sentence2, sentence3, sentence4, sentence5, sentence6, sentence7, sentence8, sentence9]

def make_tree(sentence):
    parsed_sentence = pfp.Parser().parse(sentence)
    tree = nltk.ImmutableTree.parse(parsed_sentence)
    #tree.draw()
    return tree

def sanitize_sentence(sentence):
        
    #converts to ascii
    if isinstance(sentence, unicode):
        sentence = sentence.encode("ascii", "ignore")
    
    #takes out restricted (R) sign
    if "\xc2\xae" in sentence:
        sentence = sentence.replace("\xc2\xae", "")
    
    if "()" in sentence or "( )" in sentence:
        sentence = sentence.replace("()", "")
        sentence = sentence.replace("( )", "")
    
    if len(re.findall(r'\w+', sentence)) > 38:
        sentence = "x"

    return sentence
        
        # test for "()" or "( )" and delete that if present
        


def traverse(t):
    s_find = re.compile("^S")
    vp_find = re.compile("^VP")
    try:
        t.node
    except AttributeError:
        if "DAT" in t: 
            pos_list.append(t)
            # adds index of this DAT to q1 index list
            pos_length = len(pos_list)
            q1_indexes.append(pos_length-1)
        elif "ADHD" in t:
            pos_list.append(t)
            pos_length = len(pos_list)
            q2_indexes.append(pos_length-1)

    else:
        # Now we know that t.node is defined
        # Then tests for presence of regex match object 
        # for clause (S) and verb phrase(VP)
        if s_find.match(t.node):
            pos_list.append(t.node)
            pos_length = len(pos_list)
            s_indexes.append(pos_length-1)
        elif vp_find.match(t.node):
            pos_list.append(t.node)
            pos_length = len(pos_list)
            vp_indexes.append(pos_length-1)
        for child in t:
            traverse(child) 



def is_pos_between(q_index_list, pos_indexes):
    is_pos_between_queries = any(pos_idx in range(q_index_list[0], q_index_list[1]) for pos_idx in pos_indexes)
    return is_pos_between_queries
    

# def is_s_between(index_list, s_indexes):
#     is_s_between_queries = any(s_idx in range(index_list[0], index_list[1]) for s_idx in s_indexes)
#     return is_s_between_queries

def find_the_things(q1_indexes, q2_indexes, vp_indexes, s_indexes):
    is_s_between_queries = False
    is_vp_between_queries = False
    for idxq1 in q1_indexes:
        for idxq2 in q2_indexes:
            index_list = [idxq1, idxq2]
            index_list.sort()
            if is_pos_between(index_list, vp_indexes):
                is_vp_between_queries = True
                break
        for idxq2 in q2_indexes:
            index_list = [idxq1, idxq2]
            index_list.sort()
            if is_pos_between(index_list, s_indexes):
                is_s_between_queries = True
                break
    
    print is_s_between_queries, "is s between"
    print is_vp_between_queries, "is vp between"
           




for sentence in sentence_list:
    vp_indexes = []
    s_indexes = []
    q1_indexes = []
    q2_indexes = []
    pos_list = []

    sentence = sanitize_sentence(sentence)
    tree = make_tree(sentence)
    traverse(tree)
    find_the_things(q1_indexes, q2_indexes, vp_indexes, s_indexes)

    print sentence
    print pos_list, "pos list"
    print vp_indexes, "vp indexes"
    print s_indexes, "s indexes"
    print q1_indexes, "q1 indexes"
    print q2_indexes, "q2 indexes"
