# test_data_file= open("en_partut-ud-train.conllu","r")
# x=test_data_file.read()
# test_data=[str(i) for i in x.split()]
# print(ar)
list_of_all_pos_tags=['ADJ' , 'ADP' , 'ADV' , 'AUX' , 'CCONJ' , 'DET' , 'INTJ' , 'NOUN' , 'NUM' , 'PART' , 'PRON' , 'PROPN' , 'PUNCT', 'SCONJ' , 'SYM' , 'VERB','X']
# AUX=VERB AUXILLARY
# PART=NONE
# DET=NONE
# ADP=NONE
# ADJ=ADJECTIVE
# ADV=NONE
# CCONJ=NONE
# NUM= NONE
# PRON=PRONOUN
# SCONJ=NONE
ref={}
for i in list_of_all_pos_tags:
	ref[i]='none'
ref['AUX']='v'
ref['ADJ']='a'
ref['NOUN']='n'
ref['VERB']='v'

import re

# This functions returns wether ith character of string s is a consonant or not
def cons(s,i):
    if re.match('[aeiou]',s[i]):
        return False
    if re.match('y',s[i]):
        if i==0:
            return True
        else:
            return (not cons(s,i-1))
    return True

#This function return the measure of word or word part, (C)(VC)^m(C)
def m(s):
    m = 0
    for i in range(0, len(s) - 1):
        if (not cons(s, i)) and cons(s, i + 1):
            m += 1
    return m


#loading various databases
base={'mice':'mouse','is':'be'}
exceps={'NNP':['gasses','fezzes','fuzzes']}
same_nouns={'NNP':['sheep','hair','species','deer','series']}
pronouns={'him':'he','his':'he','them':'they','her':'she','these':'this','those':'this','whom':'who','whose':'who','yours':'you','us':'we'}


# Storing irregular verbs and their lemmas in dictionaries
import os
path_1=os.path.abspath(os.path.dirname(__file__))
path_1=os.path.join(path_1,'irregularVerbs')
irr_verbs_file=open(path_1,'r')
irrverbs1={}
irrverbs2={}
for x in irr_verbs_file:
	ar=[i for i in x.split()]
	# print(ar)
	irrverbs2[ar[2]]=ar[0]
	irrverbs1[ar[1]]=ar[0]


# Storing comparative degree adjectives and superlative degree adjectives in dictionaries 
compAdj={}
superAdj={}
path_2=os.path.abspath(os.path.dirname(__file__))
path_2=os.path.join(path_2,'degreesAdj')
degrees_of_adj_file=open(path_2,'r')
for x in degrees_of_adj_file:
	ar=[i for i in x.split()]
	compAdj[ar[1]]=ar[0]
	superAdj[ar[2]]=ar[0]


# Functions that takes a list containing a word and its corresponding POS tag and returns the lemma.
def lemmr_func(sy):
    s=sy[0]
    tag=sy[1]
    s=s.lower()

    #rule for proper noun
    if tag=='PN':
    	pass
    elif tag=='NNS' or tag=='nns' or tag=='nnps' or tag=='NNPS' or tag=='n': #rule for other nouns plural
    	t=s[:len(s)-2]
    	if s not in exceps['NNP'] and s not in same_nouns['NNP']:
	    	if re.match('[a-z]*ies$',s) and m(s[:len(s)-3]):
	    		print(1)
	    		s=s[:len(s)-3]+'y'
	    	elif re.match('[a-z]*es$',s) and m(s[:len(s)-2])>0 and ( re.match('[a-z]*zz$',s[:len(s)-2]) or re.match('[a-z]*ss$',s[:len(s)-2]) ):
	    		print(2)
	    		s=s[:len(s)-3]
	    	elif re.match('[a-z]*es$',s) and m(s[:len(s)-2])>0 and ( re.match('[a-z]*s$',t) or re.match('[a-z]*ss$',t) or re.match('[a-z]*sh$',t) or re.match('[a-z]*ch$',t) or re.match('[a-z]*x$',t) or re.match('[a-z]0*ch$',s) ):
	    		print(8)
	    		s=s[:len(s)-2]
	    	elif re.match('[a-z]*ves$',s) and m(s[:len(s)-3])>0:
	    		print(3)
	    		s=s[:len(s)-3]+'f'
	    	elif re.match('[a-z]*ves$',s) and m(s[:len(s)-3])==0:
	    		print(4)
	    		s=s[:len(s)-3]+'fe'
	    	elif re.match('[a-z]*es$',s) and m(s[:len(s)-2])>0 and s[-3]=='o':
	    		print(6)
	    		s=s[:len(s)-2]
	    	elif re.match('[a-z]*s$',s) and m(s[:len(s)-1])>0 and s[-2]!='y' and s[-3]!='o':
	    		print(5)
	    		s=s[:len(s)-1]
	    	elif re.match('[a-z]*i$',s) and m(s[:len(s)-1])>0:
	    		print(7)
	    		s=s[:len(s)-1]+'us'
    elif tag=='v' or tag=='vb' or tag=='vbd' or tag=='vbg' or tag=='vbn' or tag=='vbp' or tag=='vbz': # rules for verbs
        if s in irrverbs1:
            s=irrverbs1[s]
        elif s in irrverbs2:
            s=irrverbs2[s]
        elif re.match('[a-z]*ing$',s) and m(s[:len(s)-3])>0:
            s=s[:len(s)-3]
            if s[-1]=='v' or s[-1]=='c' or ( cons(s,-1) and (not cons(s,-2)) and cons(s,-3) ):
                s+='e'
            elif s[-1]==s[-2] and not (s[-1]=='l' or s[-1]=='s'):
                s=s[:len(s)-1]
        elif re.match('[a-z]*ied$',s) and m(s[:len(s)-3])>0:
        	s=s[:len(s)-3]
        	s+='y'
        elif re.match('[a-z]*ed$',s) and m(s[:len(s)-2])>0:
            s=s[:len(s)-2]
            if s[-1]=='v' or s[-1]=='c' or s[-1]=='s':
                s+='e'
            elif s[-1]==s[-2] and not (s[-1]=='l' or s[-1]=='s'):
                s=s[:len(s)-1]
        elif re.match('[a-z]*d$',s) and m(s[:len(s)-1])>0:
            s=s[:len(s)-1]
            if s[-1]=='v' or s[-1]=='c':
                s+='e'
            elif s[-1]==s[-2] and not (s[-1]=='l' or s[-1]=='s'):
                s=s[:len(s)-1]
    elif tag=='jjr' or tag=='JJR' or tag=='a': #rules for comparative degree adjectives
        if s in compAdj:
            s=compAdj[s]
        elif re.match('[a-z]*er$',s):
            if re.match('[a-z]*ier$',s):
                s=s[:len(s)-3]+'y'
            else:
                s=s[:len(s)-2]
        elif s in superAdj:
            s=superAdj[s]
        elif re.match('[a-z]*est$',s):
            if re.match('[a-z]*iest$',s):
                s=s[:len(s)-4]+'y'
            else:
                s=s[:len(s)-3]
    elif tag=='PRON':
    	if s in pronouns:
    		s=pronouns[s]
    return s


# Main function
# if __name__=="__main__":
# 	count_correct_output=0
# 	total_count=0
# 	for i in range(0,len(test_data)):
# 		if test_data[i] in list_of_all_pos_tags and test_data[i-3].isnumeric():
# 			x=test_data[i-1]
# 			y=test_data[i-2]
# 			x=x.lower()
# 			y=y.lower()
# 			arg=[]
# 			arg.append(y)
# 			arg.append(ref[test_data[i]])
# 			print(y,x,lemmr_func(arg),test_data[i],ref[test_data[i]])
# 			if lemmr_func(arg)==x:
# 				count_correct_output+=1
# 			total_count+=1
# 	print("accuracy: ",end=" ")
# 	print(count_correct_output/total_count)