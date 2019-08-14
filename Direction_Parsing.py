#parsing sentences
import nltk
import os
import csv
import sys
from nltk.stem.snowball import SnowballStemmer


def traverse_tree(tree):
    #Traverses a given subtree to find the potential directional word. (JJ, RB, VB)
    #Returns the leaf of the value in the possible directional word position.
    new_tree = tree
    for subtree in tree:
        if type(subtree) == nltk.tree.Tree:
            new_tree = traverse_tree(subtree)

    return new_tree


def traverse_tree_Extract_Numbers(tree, number_list):
	#Traverses a subtree to extract the two numbers in the sentence to signify directionality. 
	#Returns a list of the leaves of CD Nodes (numbers). 
	new_tree = tree
	for subtree in tree:
		if type(subtree) == nltk.tree.Tree:
			if subtree.label() == 'CD':
				number_list.append(subtree)
			new_tree = traverse_tree_Extract_Numbers(subtree, number_list)

	return number_list

def search_directionality(tree):
	#Searches through the document of directional words and return if the word matches the 
	#Returns Directionality of the tree. 
	rtnElement = None 
	stemmer = SnowballStemmer("english")
	try:
		elem = tree[0][0]
		elem = stemmer.stem(elem)

		file = open("Dictionaries/Direction_Indicators_Stemmed.csv")
		reader = csv.reader(file, delimiter=',')

		for row in reader:
			if elem == row[0]:
				rtnElement = row[1]

		return rtnElement
	except Exception as e:
		print("exception: search_directionality", e)
		return rtnElement


def compare_numbers(num_list):
	#Extract the numbers in the numbers and assign directionality. 
	#Returns Directionality.
	rtnDirection = None

	if len(num_list) < 2: 
		#print("empty list")
		return rtnDirection

	try:
		elem1 = num_list[0][0][0]
		elem2 = num_list[1][0][0]

		numElem1 = (float) (elem1)
		numElem2 = (float) (elem2)

		if(numElem1 <= numElem2): 
			rtnDirection = "Up"
		else:
			#greater than, ie. goes down...
			rtnDirection = "Down"
		return rtnDirection

	except ValueError:
		#print("Error: compare_numbers: Invalid Number Comparison with Elements:", elem1, "&", elem2)
		return rtnDirection

	except Exception as e:
		print("Error: compare_numbers:", e)
		return rtnDirection


def Parse_For_Grammar_Scheme_1(sentence):
	#Searches a given sentence for clues to its directionality to tag the Lead or Lag indicator as Up or Down. 
	#Returns a list of the tags for the sentence. 

	#Define return Element 
	rtnDirectionality = None

	#Defined Grammar Scheme.
	grammar1_rule_1 = "JJ : {<JJ.*>*}"
	grammar1_rule_2 = "VB:{<VB.*>}"
	grammar1_rule_3 = "NP : {(<NNS|NN>)*}"
	grammar1_rule_4 = "NPP : {<NNP|NNPS>}"
	grammar1_rule_5 = "RB : {< RB.* >}"
	grammar1_rule_6 = "NPJJ : {(((< NP |NPP > + < IN >< .* > * <, >)|(< JJ > * < N P |N P P > +< V B >< N P P > * < .* > * <, >))(< RB > | < DT >< N P > | < V B >< T O >))|< JJ > * < N P > (< IN >< DT > * < JJ > * < N P P > * < N P > *)* < V B > |< JJ > + < N P >< V B > |< N P |N P P > +(< (>< .* > * <) >) * ((< IN >< JJ > * < N P >)(< IN >< CD >)*)* < V B > +|< N P >< .* > +(< RB > | < JJ >)|< N P |N P P > +(< IN >< N P |N P P >)* < .* > * < V B >(< DT >< JJ >) * |< N P >< V B > (< RB > |(< T O >< DT >< N P >))|< V B >< N P |N P P > * < P OS >< JJ > * < N P > |< V B >< P RP.* >< JJ > * < N P >< IN > |< V B >< T O > * < DT > * < JJ > * < N P >< IN > * < N P > *|< N P |N P P > +(< IN >< DT > * < RB > * < JJ > * < N P |N P P >) *< RB > *(< V B >< JJ >< N P >)* < V B >(< DT >< CD >< N P >) * |(< JJ >)* < N P |N P P > + < .* > *(<, >< .* > * <, >)* < N P >}"

	grammar2_rule_7 = "CD:{<CD>}"
	grammar2_rule_8 = "NPJJ : {<NP|NPP>+(<(><.*>*<)>)*(<IN><DT>*<RB>*<JJ>*<NP|NPP>) * <RB>*(<VB><JJ><NP>)*<VB>(<DT><CD><NP>)*<NP|NPP>*<CD>*<.*>*<CD>*|<NP|NPP><IN><NP|NPP><CD><.*>*<,><VB><IN><NP|NPP><CD>}"

	#Define Parsers.
	cp1 = nltk.RegexpParser(grammar1_rule_1)
	cp2 = nltk.RegexpParser(grammar1_rule_2)
	cp3 = nltk.RegexpParser(grammar1_rule_3)
	cp4 = nltk.RegexpParser(grammar1_rule_4)
	cp5 = nltk.RegexpParser(grammar1_rule_5)
	cp6 = nltk.RegexpParser(grammar1_rule_6)

	cp7 = nltk.RegexpParser(grammar2_rule_7)
	cp8 = nltk.RegexpParser(grammar2_rule_8)

	#Tokenized and tag sentence with part-of-speech tagger.
	tokenized = nltk.word_tokenize(sentence)
	pos_sent = nltk.pos_tag(tokenized)

	result = cp1.parse(pos_sent)
	result = cp2.parse(result)
	result = cp3.parse(result)
	result = cp4.parse(result)
	result = cp5.parse(result)
	#Saved_Result will be used if we need to go to the 2nd grammar scheme.
	Saved_Result = result
	result = cp6.parse(result)

	scheme_found = False

	for subtree in result.subtrees():
		if subtree.label() == 'NPJJ':
			#Found scheme matching possible tree
			lastTree = traverse_tree(subtree)
			#Search Directionality and return Up, Down or None
			rtnDirectionality = search_directionality(lastTree)
			if rtnDirectionality != None:
				break
			

	#If the first parsing rule didn't work and there are possibly numbers in the sentence. 
	if rtnDirectionality == None:
		result = cp7.parse(Saved_Result)
		result = cp8.parse(result)
		for subtree in result.subtrees():
			if subtree.label() == 'NPJJ':
				num_list = []
				num_list = traverse_tree_Extract_Numbers(subtree, num_list)
				rtnDirectionality = compare_numbers(num_list)
				if rtnDirectionality != None:
					break
				

	return rtnDirectionality
			



