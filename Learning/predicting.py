from sklearn.ensemble import GradientBoostingClassifier
from sklearn import cross_validation
from sklearn import svm
import math

def Convert(a):
	if a == "0":
		return 0
	a = int(a)/math.fabs(int(a))
	return a

def Judge_difference_contradiction(a1,a2,a3):#judege whether there exits stroing user preference & here we assumes that contradiction brings confusion
	flag = 0 
	a1 = float(a1)
	a2 = float(a2)
	a3 = float(a3)
	# contradict judge
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

def ground_truth(file_path, prediction_type, judgement):#prediciton Path type with differnce? left_right?,judgement means how to calculate 0,1
	y = []
	result_lines = open(file_path,"r").read().split("\r")
	for line in result_lines:
		[qid,a1,a2,a3] = line.replace("\r","").split("\t")
		if prediction_type == "difference" and judgement=="contradiction":
			flag = Judge_difference_contradiction(Convert(a1),Convert(a2),Convert(a3))
			#print line.strip() + "\t" + str(flag)
			y.append(flag)
	return y

def clear_trainning_set(x,y):
	l_x = len(x)
	l_y = len(y)
	if l_x!=l_y:
		print("Error in Tranning set, break!")
	else:
		for i in range(l_y):
			if y[i]=="-1":  #judge as non-relevant
				del x[i]
				del y[i]

def get_features(file_path):
	temp = []
	lines = open(file_path,"r").readlines()
	for line in lines:
		features = line.strip().split("\t")
		temp.append(features)
	return temp

def write2X(apsects):
	X = []
	length = len(aspects[0])
	for item in aspects:
		if len(item)!=length:
			print "error! features length don't match! "

	for i in range(length):
		temp = []
		for item in aspects:
			temp = temp + item[i]
		X.append(temp)
	return X

if __name__ == "__main__":

	text_features = get_features("text_features.txt")
	query_features = get_features("query_features.txt")
	vertical_features = get_features("vertical_features.txt")
	url_features = get_features("url_features.txt")

	aspects = [query_features,vertical_features,text_features,url_features]
	#aspects = [vertical_features]
	y = ground_truth("../Result/result.txt","difference","contradiction")
	X = write2X(aspects)

	clear_trainning_set(X,y) 
	print "We got X for " + str(len(X)) +" and Y for " + str(len(y))

	clf = GradientBoostingClassifier(n_estimators=10, learning_rate=0.05,max_depth=3,random_state=0)
	#clf = svm.SVC(kernel='linear', C=1)
	test = ['average_precision','recall','f1','roc_auc']
	for item in test:
		scores = cross_validation.cross_val_score(clf,X,y,cv=3,scoring=item)
		#scores = clf.fit(x_train,y_train).score(x_test,y_test)
		print(item+" score is "+str(sum(scores)/3))



