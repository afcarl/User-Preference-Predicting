import math

def Judge(a1,a2,a3):
	flag = 0 
	a1 = float(a1)
	a2 = float(a2)
	a3 = float(a3)
	# contradict judge
	print a1
	if a1 == 0:
		if a2 == 0 or a3 == 0:
			flag = 0
		elif float(a2)*float(a3) > 0:
			flag = 1
		else:
			flag = 0
	elif a1 == -1:
		if a2 == 1 or a3 == 1:
			flag = 0
		elif a2 == 0 and a3 == 0:
			flag = 0
		else:
			flag = 1
	else:
		if a2 == -1 or a3 == -1:
			flag = 0
		elif a2 ==0 and a3 == 0:
			flag = 0
		else:
			flag = 1
	return flag 

def Left_Right_Judge(a1,a2,a3):
	flag = 0 
	a1 = float(a1)
	a2 = float(a2)
	a3 = float(a3)
	# contradict judge
	print a1
	if a1 == 0:
		if a2 == 0 or a3 == 0:
			flag = 0
		elif float(a2)*float(a3) > 0:
			if a2<0:
				flag = 1
			else:
				flag = -1
		else:
			flag = 0
	elif a1 == -1:
		if a2 == 1 or a3 == 1:
			flag = 0
		elif a2 == 0 and a3 == 0:
			flag = 0
		else:
			flag = 1
	else:
		if a2 == -1 or a3 == -1:
			flag = 0
		elif a2 ==0 and a3 == 0:
			flag = 0
		else:
			flag = -1
	return flag 



def Convert(a):
	if int(a) == 0:
		return 0
	a = int(a)/math.fabs(int(a))
	return a


def Average(p):
	n = 0 
	number = len(p)
	rsum = 0.0 
	for item in p:
		n += 1
		rsum = rsum + p[item]
	return rsum/float(number) 



def Kappa(p,r): # p is the sum of each grades and r is for each subject
	Pe = 0.0
	Pa = 0.0
	Pa = Average(r)
	for item in p:
		Pe += p[item] * p[item]
	print "Pe is " + str(Pe)
	print "Pa is " + str(Pa)
	kappa = (Pa-Pe)/(1-Pe)

	return kappa



def Add2Dict(a1,temp):
	if temp.has_key(a1):
		temp[a1] += 1
	else:
		temp[a1] = 1

result_file = open("result.txt","r")
result_lines = result_file.readlines()
count = 0
N = 1000
Result = {}
temp = {}
P = {}
#clear_id_file = open("strong_opinion.txt","w")
#clear_file = open("clear-contradict.txt","w")
for line in result_lines:
	#try:
	[qid, a1, a2, a3] = line.split("\t")
	temp[qid] = {}
	a1 = str(Convert(a1))
	a2 = str(Convert(a2))
	a3 = str(Convert(a3))
	Add2Dict(a1,temp[qid])
	Add2Dict(a2,temp[qid])
	Add2Dict(a3,temp[qid])
	Add2Dict(a1,P)
	Add2Dict(a2,P)
	Add2Dict(a3,P)
	a1_ = str(a1)
	a2_ = str(a2)
	a3_ = str(a3)
	#
	#flag = 0
	n = 0.0 
	for item in temp[qid].keys():
		n = n + float(temp[qid][item]) * float(temp[qid][item])
	Result[qid]  = (n - 3)/6.0


	#except:
	#	print "blank"


for item in P:
	P[item] = P[item]/(float(N*3))
	print item+"\t"+str(P[item])

print (Kappa(P,Result))