import csv
import nltk.data
import codecs
import os
from nltk import tokenize
import Parsing as parser

def classify_doc(fileName): 
	#Classifies the document as Positive, Negative, or Neutral based on predetermined rules for financial sentiment analysis. 
	#Returns the class name that this document belongs. 

	rtnClassification = None

	#Open predefined Rule Base.
	try: 
		file_rulebase = open("Rules/newRules.csv")
		RuleBase = csv.reader(file_rulebase, delimiter=',')
	except Exception as e:
		print("Cannot open RuleBase: Classification_Rules.csv", "\nCan't go further without this file.")
		exit()

	ruleBase = []
	for r in RuleBase: 
		ruleBase.append(r)

	#Open document and tokenize by sentence.
	try:
		doc = codecs.open(fileName)
		content = doc.read()
		tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		Sentences = tokenizer.tokenize(content)
	except Exception as e:
		print("Error opening inputted file.", e)
		exit()

	#Keeps track of the confidence of the classification. (Pos, Neg, Neu) 
	Classes = [0, 0, 0]

	#Classify doc by classifying each sentence.
	for i in range(len(Sentences)):
		#Gets tags based on pre-defined lexicon. 
		sent_tags = parser.parse_sentence(Sentences[i])

		#Converts tags to numerical representation.
		num_tags = parser.get_numerical_list(sent_tags)
		for r in ruleBase: 
			rule_r = [int(s) for s in r[0].split() if s.isdigit()]

			if num_tags == rule_r:
				#Update confidence from RuleBase to correct class
				Classes[int(r[1]) - 12] = Classes[int(r[1]) - 12] + float(r[2])
			else:
				for t in num_tags:
					if rule_r == [t]:
						Classes[int(r[1]) - 12] = Classes[int(r[1]) - 12] + float(r[2])



	if Classes[0] == max(Classes):
		return "Positive"
	elif Classes[1] == max(Classes):
		return "Negative"
	elif Classes[2] == max(Classes):
		return "Neutral"
	else:
		return "messed up"



def classify_sentence(sentence):

	#Open predefined Rule Base.
	try: 
		file_rulebase = open("Rules/newRules.csv")
		RuleBase = csv.reader(file_rulebase, delimiter=',')
	except Exception as e:
		print("Cannot open RuleBase: Classification_Rules.csv", "\nCan't go further without this file.")
		exit()

	ruleBase = []
	for r in RuleBase: 
		ruleBase.append(r)

	#Keeps track of the confidence of the classification. (Pos, Neg, Neu) 
	Classes = [0, 0, 0]


	#Gets tags based on pre-defined lexicon. 
	sent_tags = parser.parse_sentence(sentence)

	#Converts tags to numerical representation.
	num_tags = parser.get_numerical_list(sent_tags)
	for r in ruleBase: 
		rule_r = [int(s) for s in r[0].split() if s.isdigit()]

		if num_tags == rule_r:
			#Update confidence from RuleBase to correct class
			Classes[int(r[1]) - 12] = Classes[int(r[1]) - 12] + float(r[2])
		else:
			for t in num_tags:
				if rule_r == [t]:
					Classes[int(r[1]) - 12] = Classes[int(r[1]) - 12] + float(r[2])




	if Classes[0] == max(Classes):
		return "positive"
	elif Classes[1] == max(Classes):
		return "negative"
	elif Classes[2] == max(Classes):
		return "neutral"
	else:
		print("oooof")
		return "messed up"


def classify_text(text):
	#Open predefined Rule Base.
	try: 
		file_rulebase = open("Rules/newRules.csv")
		RuleBase = csv.reader(file_rulebase, delimiter=',')
	except Exception as e:
		print("Cannot open RuleBase: newRules.csv", "\nCan't go further without this file.")
		exit()

	ruleBase = []
	for r in RuleBase: 
		ruleBase.append(r)

	#Open text and tokenize by sentence.
	try:
		tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		Sentences = tokenizer.tokenize(text)
	except Exception as e:
		print("Error opening inputted file.", e)
		exit()

	#Keeps track of the confidence of the classification. (Pos, Neg, Neu) 
	Classes = [0, 0, 0]

	#Classify doc by classifying each sentence.
	for i in range(len(Sentences)):
		#Gets tags based on pre-defined lexicon. 
		sent_tags = parser.parse_sentence(Sentences[i])

		#Converts tags to numerical representation.
		num_tags = parser.get_numerical_list(sent_tags)
		for r in ruleBase: 
			rule_r = [int(s) for s in r[0].split() if s.isdigit()]

			if num_tags == rule_r:
				#Update confidence from RuleBase to correct class
				Classes[int(r[1]) - 12] = Classes[int(r[1]) - 12] + float(r[2])
			else:
				for t in num_tags:
					if rule_r == [t]:
						Classes[int(r[1]) - 12] = Classes[int(r[1]) - 12] + float(r[2])


	print(Classes)

	if Classes[0] == max(Classes):
		return "Positive"
	elif Classes[1] == max(Classes):
		return "Negative"
	elif Classes[2] == max(Classes):
		return "Neutral"
	else:
		return "messed up"

if __name__ == '__main__':
	'''
	content1 = "n"
	print("conent")
	with open("LiveSentAnalysis.txt", encoding = "ISO-8859-1") as f:
		content1 = f.read().replace('\n', '')
		print(classify_text(content1))

	'''
	'''
	while True:
		with open("LiveSentAnalysis.txt", 'r') as f: 
			newC = f.read().replace('\n', '')
			if(content1 != newC):

				print("compare theses old, new: ", content1,",", newC)
				content1 = newC
				#print("inside")
				try:
					print("beefore classify")
					cs = classify_text(newC)
					#print("after Classify")
					print()
					#
					#content1 = f.read().replace('\n', '')
				except Exception as e:
					print("why?:::", e)

	'''


	with open("DataSets/DS100.txt", encoding = "ISO-8859-1") as f: 
			content = f.readlines()
			
			class_tags = []
			right = 0
			wrong = 0
			counterrrr = 0
			wrongNeg = 0
			wrongPos = 0
			wrongNeu = 0

			totalPos = 0
			totalNeg = 0
			totalNeu = 0

			for c in content:
				counterrrr += 1
				split_c = c.split("@",1)
				class_tags.append(split_c[1])
				tempTags = parser.parse_sentence(split_c[0])
				#print("senetence:", split_c[0])
				#print("tags:", tempTags)
				#print("Actual Classification:", split_c[1])
				cs = classify_sentence(split_c[0])
				if "negative" in split_c[1]:
					totalNeg +=1
				elif "positive" in split_c[1]:
					totalPos +=1
				elif "neutral" in split_c[1]:
					totalNeu += 1
				else:
					print("goofed", split_c[1])


				#print("My Classification:", cs)
				if cs in split_c[1]: 
					right = right +1
					#print("right!!")
				else:
					if "negative" == cs:
						wrongNeg +=1
					elif "positive" == cs:
						wrongPos +=1
					elif "neutral" == cs:
						wrongNeu += 1
					else:
						print("goofed", cs)

					wrong = wrong + 1
				#print("---------------------------")
				#print("")
				#if counterrrr == 100:
				#	break


			total = right + wrong

			print("right:", right)
			print("wrong:", wrong)
			print("accuracy:", right / total)

			print("wrong negative:", wrongNeg, "   %:out of wrong: ", wrongNeg / wrong)
			print("wrong positive:", wrongPos, "   %:out of wrong: ", wrongPos / wrong)
			print("wrong negative:", wrongNeu, "   %:out of wrong: ", wrongNeu / wrong)
			
			print("total Posiitve:", totalPos, " percent right:", 1 - (wrongPos / totalPos))
			print("total Negative:", totalNeg, " percent right:", 1 - (wrongNeg / totalNeg))
			print("total Neutral:", totalNeu, " percent right:", 1 - (wrongNeu / totalNeu))
