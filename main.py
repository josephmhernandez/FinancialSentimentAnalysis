#Sentiment Analysis: Hierarchal Sentiment Classifier
import os
import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english")


def Create_LM_Dictionary(): 
	#Loads LM dictionary for category: Polarity Sentiment Words
	# User defined file pointer to LM dictionary
	MASTER_DICTIONARY_FILE = r'/home/joseph/Documents/Csce 470/Task2/' + 'LoughranMcDonald_MasterDictionary_2014.csv'


	file = open(MASTER_DICTIONARY_FILE)
	reader = csv.reader(file, delimiter=',')
	lm_dict = []
	next(reader)
	for row in reader:
		if float(row[7]) > 0: 
			pair = (row[0].lower(), "Negative")
			lm_dict.append(pair)
		elif float(row[8]) > 0: 
			pair = (row[0].lower(), "Positive")
			lm_dict.append(pair)

	lm_dict = list(dict.fromkeys(lm_dict))
	#print(lm_dict)
    

	with open('LM_Dictionary.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(lm_dict)
	csvFile.close()

def Create_Indicator_Category():
	file = open("directionality.txt")
	reader = csv.reader(file, delimiter=',')
	new_list = []

	for j in reader:
		for i in j:
			
			tempName = i
			tempName = tempName.lstrip()
			tempName = tempName.rstrip()
			tempName = ''.join(p for p in tempName if not p.isdigit())
			tempName = tempName.lower()
			print(tempName)
			myInputstr = input("1=> UP\t2=> DOWN\t 3=>Edit\t 4=> SKIP")
			myInput = float(myInputstr)
			if(myInput == 1):
				new_list.append((tempName, "Up"))
			elif myInput == 2:
				new_list.append((tempName, "Down"))
			elif myInput == 4:
				print("Skipped!")
			else:
				tempName = input("Enter new Name: ")
				direction = input("Direction: ")
				new_list.append((tempName, direction))
	#Gets list of directional words and labels them up or down.
	print(new_list)
	with open('Direction_Indicators.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(new_list)
	csvFile.close()

def Create_ind_cateogory(): 
	file = open("Indicators.txt")
	reader = csv.reader(file, delimiter=',')
	new_list = []

	for j in reader:
		for i in j:
			
			tempName = i
			tempName = tempName.lstrip()
			tempName = tempName.rstrip()
			tempName = ''.join(p for p in tempName if not p.isdigit())
			tempName = tempName.lower()

			print(tempName)
			myInputstr = input("1=> LeadInd\t2=> LagInd\t 3=>Edit\t 4=> SKIP")
			myInput = float(myInputstr)
			if(myInput == 1):
				new_list.append((tempName, "LeadInd"))
			elif myInput == 2:
				new_list.append((tempName, "LagInd"))
			elif myInput == 4:
				print("Skipped!")
			else:
				tempName = input("Enter new Name: ")
				direction = input("Direction: ")
				new_list.append((tempName, direction))
	#Gets list of directional words and labels them up or down.
	print(new_list)
	with open('Lead_Lag_Indicators.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(new_list)
	csvFile.close()
	


if __name__ == '__main__':
	#Run once to get the LM Dictionary 
	Create_LM_Dictionary()
	#Create_Indicator_Category()
	#Create_ind_cateogory()
	print("Hello")

	#Load 