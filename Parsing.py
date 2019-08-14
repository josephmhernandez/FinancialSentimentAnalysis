#parsing sentences
import nltk
import os
import csv
import sys
from nltk.stem.snowball import SnowballStemmer

import Direction_Parsing as direction_parser

def get_numerical_list(tag_list):
	#Gets tags in text form and transforms them into numbers representing the tags.
	#Returns list of numerical values. 
	rtnList = []
	if len(tag_list) == 0: 
		rtnList.append(11)
	for tag in tag_list: 
		if tag == "Positive": 
			rtnList.append(1)
		elif tag == "Negative": 
			rtnList.append(2)
		elif tag == "LagInd":
			rtnList.append(3)
		elif tag == "LeadInd":
			rtnList.append(4)
		elif tag == "LagInd::Up":
			rtnList.append(5)
		elif tag == "LagInd::Down":
			rtnList.append(6)
		elif tag == "LeadInd::Up":
			rtnList.append(7)
		elif tag == "LeadInd::Down":
			rtnList.append(8)
		elif tag == "Up":
			rtnList.append(9)
		elif tag == "Down":
			rtnList.append(10)
		else: 
			print("oof: tag:", tag)

	return sorted(rtnList)

def find_indicators(sentence):
	#Searches through the sentence looking for Lagging and Leading indicators. 
	#Returns either LagInd, LeadInd, or None
	stemmer = SnowballStemmer("english")
	tokenizer = nltk.RegexpTokenizer(r'\w+')
	tokenized = tokenizer.tokenize(sentence.lower())

	stem_sent = [stemmer.stem(x) for x in tokenized]
	
	sent = ""
	for x in stem_sent:
		sent = sent + x + " "
	sent.rstrip()

	try: 
		file = open("Dictionaries/Lead_Lag_Indicators_Stemmed.csv")
		reader = csv.reader(file, delimiter=',')
		for row in reader: 
			if sent.find(row[0]) > 0: 
				return row[1]
	except Exception as e: 
		print("ERROR: find_indicators:", e)

	return None

def find_directionality(sentence): 
	#Searches through the sentence looking for words that match a direction of the sentence.
	#Returns a list of the directions used in the sentence. 
	rtn_list = []

	stemmer = SnowballStemmer("english")
	tokenizer = nltk.RegexpTokenizer(r'\w+')
	tokenized = tokenizer.tokenize(sentence.lower())

	stem_sent = [stemmer.stem(x) for x in tokenized]

	sent = ""
	for x in stem_sent: 
		sent = sent + x + " "

	try: 
		file = open("Dictionaries/Direction_Indicators_Stemmed.csv")
		reader = csv.reader(file, delimiter=',')
		for row in reader: 
			if (row[0]+" ") in sent:
				rtn_list.append(row[1])
	except Exception as e:
		print("Error: find_directionality()", e)

	return rtn_list

def find_polarity(sentence): 
	#Searches throught the sentence and returns words that have meaningful polarity in a financial text document.
	#Returns a list of polarity tags for the sentence. 
	rtn_list = []

	stemmer = SnowballStemmer("english")
	tokenizer = nltk.RegexpTokenizer(r'\w+')
	sentence.lower()

	try: 
		file = open("Dictionaries/LM_Dictionary.csv")
		reader = csv.reader(file, delimiter=',')
		for row in reader: 
			if (row[0]+" ") in sentence:
				rtn_list.append(row[1])
	except Exception as e:
		print("Error: find_polarity()", e)

	return rtn_list

def parse_sentence(sentence):
	#Tags a sentence based on the finanicial lexicon.
	#Returns list of tags. 

	rtnTags = []

	#Search for indicators in the sentence.
	new_tag = find_indicators(sentence)
	
	skip_directionality = False

	if new_tag != None: 
		#Attach direction to grammar scheme. 
		temp_direction = direction_parser.Parse_For_Grammar_Scheme_1(sentence)
		if temp_direction == None: 
			rtnTags.append(new_tag)
		else:
			#Has directionality.
			skip_directionality = True 
			temp_tag = new_tag + "::" + temp_direction
			rtnTags.append(temp_tag)

	#Search for directionality in the sentence (If no indicator direction was found).
	if not skip_directionality: 
		temp_tags = []
		temp_tags = find_directionality(sentence) 
		#Update return tags. 
		for tag in temp_tags: rtnTags.append(tag)


	#Search for the positive/negative words in the sentence.
	temp_tags = []
	temp_tags = find_polarity(sentence)

	for tag in temp_tags: rtnTags.append(tag)

	#Get rid of duplicates.
	rtnTags = list(dict.fromkeys(rtnTags))
	
	return rtnTags


