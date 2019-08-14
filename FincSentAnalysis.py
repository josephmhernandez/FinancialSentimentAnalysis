#Financial Sentiment Analysis

'''
The purpose for this project is to perform sentiment analysis on financial 
documents pulled from various websites through Yahoo Finance. The techniques 
utilized in this project were based off a paper title "Sentiment Analysis 
of Financial News Articles using Performance Indicators" by Srikumar 
Krishnamoorthy. This project uses a financial specific lexicon that is 
a compilation of positive & negative financial terms, directionality terms,
and leading & lagging performance indicators. 
'''
import Direction_Parsing as direction_parser
import Parsing as parser 
import Train as trainer
import Classify as classifeir

if __name__ == '__main__':
	td = ["DS100", "DS75", "DS66"]

	trainer.TrainingMatrix("DataSets/DS100.txt", results_csv = "NewRulesForME.csv")
	'''
	for t in td:
		trainer.TrainingMatrix(t+".txt", results_csv = t+"_rulesManip.csv")
	'''
	trainer.get_rules()
	print("done")
	
