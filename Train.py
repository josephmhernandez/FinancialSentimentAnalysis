import nltk
import csv
import Parsing as parser
import pyfpgrowth

class TrainingMatrix():

	def __init__(self, fileLocation, results_csv = None):
		self.fileName = fileLocation
		if results_csv == None:
			self.csvFileName = "_TrainingMatrix.csv"
		else:
			self.csvFileName = results_csv
		self._make_matrix()

	def _make_matrix(self): 
		first_row = ["sentence", "Pos", "Neg", "LagInd", "LeadInd", "LagInd::Up", "LagInd::Down", "LeadInd::Up", "LeadInd::Down", "Up", "Down", "Class"]
		parse_tags = []
		print("here")
		with open(self.fileName, encoding = "ISO-8859-1") as f: 
			content = f.readlines()
			
			class_tags = []
			
			for c in content:
				split_c = c.split("@",1)
				class_tags.append(split_c[1])
				tempTags = parser.parse_sentence(split_c[0])
				parse_tags.append(tempTags)

		
		cor_class_tags = []
		for c in class_tags: 
			if "positive" in c: 
				cor_class_tags.append("Positive")
			elif "negative" in c: 
				cor_class_tags.append("Negative")
			elif "neutral" in c:
				cor_class_tags.append("Neutral")
			else:
				print("ERROR")
		
		if(len(parse_tags) == len(cor_class_tags)):
			print("good to go")
		else:
			print("u r dumb") 


		#for tags in parse_tags: 
		#	tag_str = get_binary(tags)
		

		train_mat = []
		other_mat = []

		for i in range(len(parse_tags)):
			tag_str = get_numerical(parse_tags[i], cor_class_tags[i])
			train_mat.append((i+1, parse_tags[i], cor_class_tags[i]))
			other_mat.append((tag_str, cor_class_tags[i]))

		'''
		with open(self.csvFileName, 'w') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerows(first_row)
			writer.writerows(train_mat)
			csvFile.close()
		'''
		
		with open(self.csvFileName, 'w') as csvfile: 
			writer = csv.writer(csvfile)
			writer.writerows(other_mat)
		


		print("traing matrix is done-so and has been saved: ")
		'''
		with open(csvFileName, 'w') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerows(first_row)

			writer.writerows(binaryRows)
		'''
def get_binary(tag_list): 
	pos = False
	neg = False
	LagInd = False
	LeadInd = False
	LagInd_Up = False
	LagInd_Down = False
	LeadInd_Up = False
	LeadInd_Down = False
	Up = False
	Down = False

	rtnStr = ""

	for tag in tag_list: 
		if tag == "Positive": 
			pos = True
			rtnStr
		elif tag == "Negative": 
			neg = True
		elif tag == "LagInd":
			LagInd = True
		elif tag == "LeadInd":
			LeadInd = True
		elif tag == "LagInd::Up":
			LagInd_Up = True
		elif tag == "LagInd::Down":
			LagInd_Down = True
		elif tag == "LeadInd::Up":
			LeadInd_Up = True
		elif tag == "LeadInd::Down":
			LeadInd_Down = True
		elif tag == "Up":
			Up = True
		elif tag == "Down":
			Down = True
		else: 
			print("ur dumb. ", tag)


	rtnStr = "" + str(pos*1) + str(neg*1) + str(LagInd*1) + str(LeadInd*1) + str(LagInd_Up*1) + str(LagInd_Down*1) + str(LeadInd_Up*1) + str(LeadInd_Down*1) + str(Up*1) + str(Down*1)
	#for i in range(len(rtnStr)):

	return rtnStr

def get_numerical(tag_list, pol):
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
			print("ur dumb. ", tag)

	'''
	if pol == "Positive": 
		rtnList.append(12*1)
	elif pol == "Neutral":
		rtnList.append(14*1)
	elif pol == "Negative":
		rtnList.append(13*1)
	else: 
		print("u r dumb",pol, "...")
	'''	
	

	return sorted(rtnList)

def get_rules(): 
	file = open("NewRulesForME.csv")
	reader = csv.reader(file, delimiter=',')
	transactions = []
	for row in reader:
		transactions.append(row)

	
	patterns = pyfpgrowth.find_frequent_patterns(transactions, 3)

	rules = pyfpgrowth.generate_association_rules(patterns, 0.60)

	print(rules)
	for i in rules: 
		print(i)



	'''
	#content = reader.readlines()
	for row in reader: 
		print(len(row))
		break

	count = [0,0,0,0,0,0,0,0,0,0]

	#with open("trainMatSave.csv", encoding = "ISO-8859-1") as f: 
	file = open("trainMatSave.csv")
	reader = csv.reader(file, delimiter=',')
		#content = f.readlines()
	for r in reader:
		for i in range(len(r[1])):
			if (r[1])[i] == "1":
				count[i] = count[i] + 1
		
		
	#[  		 	 			111, 			40, 			14,]
	'''
	#Order Neg, Up, LagInd, LeadInd, Pos, LagInd::Up, Down, LagInd::Down, LeadInd::Up, LeadInd::Down
	#[207, 	656, 	317, 		287, 	180, 			111, 			40, 			14, 			330, 	113]
	#"Pos", "Neg", "LagInd", "LeadInd", "LagInd::Up", "LagInd::Down", "LeadInd::Up", "LeadInd::Down", 	"Up", 	"Down"]
	
	#for row in reader: 


