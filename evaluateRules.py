
import csv

def test_Rule(rule, rule_rtn): 
	file = open("Rules/rulesManip.csv")
	reader = csv.reader(file, delimiter=']')

	tneu = 0
	tpos = 0
	tneg = 0
	fneu = 0
	fpos = 0
	fneg = 0

	for row in reader: 
		new_row_0 = [int(s) for s in row[0].split() if s.isdigit()]
		#print(row)
		#print("row[0]:", row[0])
		#print("new_row_0", new_row_0)

		
		new_row_1 = row[1].replace(' ', '')
		#print("new_row_1", new_row_1)

		if new_row_0 == rule: 
			if new_row_1 == "Positive":
				tpos = tpos + 1
			elif new_row_1 == "Negative":
				tneg = tneg + 1
			elif new_row_1 == "Neutral":
				tneu = tneu + 1
			else:
				print("Big oof1", new_row_0)
		else:
			if new_row_1 == "Positive":
				fpos = fpos + 1
			elif new_row_1 == "Negative":
				fneg = fneg + 1
			elif new_row_1 == "Neutral":
				fneu = fneu + 1
			else:
				print("Big oof2", new_row_0)

	#writes the matrix for observed value: 
	print(rule, "Pos", "Neu", "Neg", "Total")
	print("true", tpos, tneu, tneg, tpos+tneg+tneu)
	print("false", fpos, fneu, fneg, fpos+fneg+fneu)
	print("total", tpos+fpos, tneu+fneu, tneg+fneg, fpos+fneg+fneu+tpos+tneg+tneu)
	print()

	#compute the expected value matrix: 
	T6 = fpos+fneg+fneu+tpos+tneg+tneu
	T5 = tneg+fneg
	T4 = tneu+fneu
	T3 = tpos+fpos
	T2 = fpos+fneg+fneu
	T1 = tpos+tneg+tneu

	E1 = (T3 * T1) / T6
	E2 = (T4 * T1) / T6
	E3 = (T5 * T1) / T6
	E4 = (T3 * T2) / T6
	E5 = (T4 * T2) / T6
	E6 = (T5 * T2) / T6
	#print(rule, "Pos", "Neu", "Neg", "Total")
	#print("true", E1, E2, E3, T1)
	#print("false", E4, E5, E6, T2)
	#print("total", T3, T4, T5, T6)
	#print()

	X1 = ((tpos - E1)**2) / E1
	X2 = ((tneu - E2)**2) / E2
	X3 = ((tneg - E3)**2) / E3
	X4 = ((fpos - E4)**2) / E4
	X5 = ((fneu	- E5)**2) / E5
	X6 = ((fneg - E6)**2) / E6

	Chi2 = X1 + X2 + X3 + X4 + X5 + X6

	supP = T1
	supC = 0
	if rule_rtn == 12:
		supC = T3
	elif rule_rtn == 13:
		supC = T5
	elif rule_rtn == 14:
		supC = T4
	else:
		print("big oof3:rule_rtn", rule_rtn)
	
	T = T6

	e_val =  float((1 / (supP * supC)) + (1/(supP * (T - supC))) + (1/((T - supP) * supC)) + (1 /((T - supP)*(T - supC))))

	maxChi2 = ((min(supP,supC) - ((supC * supP)/T))**2) * T * e_val

	weighted_chi2 = (Chi2) / (maxChi2)

	#print("weighted_chi2: ", weighted_chi2, "\n")
	return weighted_chi2

def write_rules(fileName, rules):
	rule_mat = []

	for r in rules: 
		confidence = test_Rule(r[0], r[1])
		str_rule = ""
		for i in r[0]:
			str_rule = str_rule + str(i) + " "

		#print([int(s) for s in str_rule.split() if s.isdigit()])
		rule_mat.append((str_rule, r[1], confidence))

	#print(rule_mat)
	for r in rule_mat: 
		print(r)
	with open(fileName, 'w') as csvfile: 
		writer = csv.writer(csvfile)
		writer.writerows(rule_mat)

if __name__ == '__main__':
	#r = [3, 9, 10]
	'''
	rules = [([1, 2, 10], 13), 
			([3, 9, 10], 13),
			([2, 9, 10], 13), 
			([3, 10], 13), 
			([2, 3, 10], 13), 
			([2, 10], 13),
			([1, 5], 12),
			([1, 4, 9], 12),
			([1, 2, 4, 9], 12), 
			([1, 2, 3, 9], 12), 
			([1, 2, 3], 12), 
			([11], 14),
			([2], 14),
			([1, 3], 12),
			([1, 9], 12), 
			([3, 9], 12)
			]
	rules = [([1], 14),
			([2], 14),
			([3], 14),
			([4], 14),
			([5], 14),
			([6], 14),
			([9], 14),
			([10], 14),
			]

	'''
	# rules = [([1, 5], 12),
	# 		([1, 2, 3], 12),
	# 		([4, 10], 13),
	# 		([2, 3, 10], 13),
	# 		([2, 6], 13),
	# 		([1, 6],12),
	# 		([2, 10],14),
	# 		([3, 10],13),
	# 		([10],13),
	# 		([11],14),
	# 		]

	rules = [([1, 2, 10], 13),
			([1, 2, 3, 9], 12),
			([1, 10], 13),
			([1, 2, 9], 12),
			([1, 3, 9], 12),
			([1, 5], 12),
			([2, 9, 10], 13),
			([1, 2, 3], 12),
			([2, 3, 10], 13),
			([2, 4], 14),
			([1, 3], 12),
			([4], 14),
			([3, 10], 13),
			([10], 13),
			([11], 14),
			]

	write_rules("newRules.csv", rules)

	#r_rtn = 13

	

