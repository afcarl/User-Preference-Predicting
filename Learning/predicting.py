from sklearn.ensemble import GradientBoostingClassifier
from sklearn import cross_validation
from sklearn import svm
import math
from sklearn.metrics import *
import matplotlib.pyplot as plt
import numpy as np


def Convert(a):
	#if a == "0" or a=="-1" or a =="1":
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

def Judge_difference_vote(a1,a2,a3):#judege whether there exits stroing user preference & here we assumes that contradiction brings confusion
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
			flag = -1
	elif a1 == -1:
		if a2 == 1 or a3 == 1:
			flag = -1
		elif a2 == 0 and a3 == 0:
			flag = 0
		else:
			flag = 1
	else:
		if a2 == -1 or a3 == -1:
			flag = -1
		elif a2 ==0 and a3 == 0:
			flag = 0
		else:
			flag = 1
	#print str(a1) + "\t" + str(a2) + "\t" + str(a3) + "\t" + str(flag)
	return flag 

def Judge_left_right_vote(a1,a2,a3):#judege whether there exits stroing user preference & here we assumes that contradiction brings confusion
	flag = 0 
	a1 = float(a1)
	a2 = float(a2)
	a3 = float(a3)
	# contradict judge
	if a1 == 0:
		if a2 == 0 or a3 == 0:
			flag = -1
		elif a2 == 1 and a3 == 1:
			flag = 0
		elif a2 == -1 and a3 == -1:
			flag = 1
		else:
			flag = -1
	elif a1 == -1:
		'''if a2 == -1 or a3 == -1:
			flag = 1
		elif a2 == 1 and a3 == 1:
			flag = 0
		else:
			flag = -1'''
		if a2 == 0 and a3 == 0:
			flag = -1
		elif a2 == 1 or a3 == 1:
			flag = -1
		else:
			flag = 1
	else:
		'''if a2 == 1 or a3 == 1:
			flag = 0
		elif a2 ==-1 and a3 == -1:
			flag = 1
		else:
			flag = -1'''
		if a2 == 0 and a3 == 0:
			flag = -1
		elif a2 == -1 or a3 == -1:
			flag = -1
		else:
			flag = 0
	#print str(a1) + "\t" + str(a2) + "\t" + str(a3) + "\t" + str(flag) 		
	return flag 
def Judge_left_right_vote_no_filter(a1,a2,a3):#judege whether there exits stroing user preference & here we assumes that contradiction brings confusion
	flag = 0 
	a1 = float(a1)
	a2 = float(a2)
	a3 = float(a3)
	if a1 == 0:
		if a2 == 0 or a3 == 0:
			flag = -1
		elif a2 == 1 and a3 == 1:
			flag = 0
		elif a2 == -1 and a3 == -1:
			flag = 1
		else:
			flag = -1
	elif a1 == -1:
		if a2 == -1 or a3 == -1:
			flag = 1
		elif a2 == 1 and a3 == 1:
			flag = 0
		else:
			flag = -1
	else:
		if a2 == 1 or a3 == 1:
			flag = 0
		elif a2 ==-1 and a3 == -1:
			flag = 1
		else:
			flag = -1	
	return flag 

def ground_truth(file_path, prediction_type, judgement, top):#prediciton Path type with differnce? left_right?,judgement means how to calculate 0,1
	y = []
	result_lines = open(file_path,"r").readlines()
	count = 0
	for line in result_lines:
		count += 1
		if count > top:
			break
		#print line
		[qid,a1,a2,a3] = line.replace("\n","").strip().split("\t")
		if prediction_type == "difference" and judgement=="contradiction":
			flag = Judge_difference_contradiction(Convert(a1),Convert(a2),Convert(a3))
			print line.strip() + "\t" + str(flag)
		elif prediction_type == "difference" and judgement == "vote":
			flag = Judge_difference_vote(Convert(a1),Convert(a2),Convert(a3))
			print line.strip() + "\t" + str(flag)
		elif prediction_type == "left_right" and judgement == "vote":
			flag = Judge_left_right_vote(Convert(a1),Convert(a2),Convert(a3))
		elif prediction_type == "left_right" and judgement == "vote_no_filter":
			flag = Judge_left_right_vote_no_filter(Convert(a1),Convert(a2),Convert(a3))
		y.append(flag)
	return y

def clear_trainning_set(x,y):
	delete_list = []
	l_x = len(x)
	l_y = len(y)
	if l_x!=l_y:
		print("Error in Tranning set, break!")
	else:
		for i in range(l_y):
			if y[i]== -1 :  #judge as non-relevant
				delete_list.append(i)
	count = 0
	for item in delete_list:
		item = item - count
		del x[item]
		del y[item]
		count += 1
	print "delete elements have " + str(count) + "\t" +str(len(delete_list))

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

	aspects = [vertical_features,text_features]
	#aspects = [url_features]
	#y = ground_truth("../Result/result.txt","difference","vote",1000)
	y = ground_truth("../Result/result.txt","left_right","vote",1000)
	X = write2X(aspects)[:1000]

	clear_trainning_set(X,y)
	y1 = 0 
	y0 = 0
	for i in range(len(y)):
		if y[i] == 1:
			y1 += 1
		else:
			y0 += 1

	print "We got X for " + str(len(X)) +" and Y for " + str(len(y))
	print "we have " + str(y1) + "for 1 and " + str(y0) + " for 0" 
	clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.01,max_depth=3,random_state=0)
	#clf = svm.SVC(C=1.0, kernel='rbf', degree=3, gamma=0.0, coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, random_state=None)
	test = ['accuracy','recall_macro','f1_macro','roc_auc']
	for item in test:
		scores = cross_validation.cross_val_score(clf,X,y,cv=5,scoring=item)
		print(item+" score is "+str(sum(scores)/5))
		#print scores 
	#clf.fit(X[:800],y[:800])
	#X_ = X[200:300]
	#print clf.predict_proba(X_)



'''
	print "Majority Voting"
	if y1 > y0:
		y_major = [ 1 for i in range(len(y)) ]
	else:
		y_major = [ 0 for i in range(len(y)) ]
	score = accuracy_score(y, y_major)
	print "accuracy score is " + str(score)
	score = 0.5
	print "recall_macro score is " + str(score)
	precision = float(max(y1,y0))/float(len(y_major))
	score = 2.0/(1/precision+2.0)
	print "f1_macro score is " + str(score)
	print "roc_auc score is " + str(roc_auc_score(y, y_major))
'''
'''
	x_train, x_test, y_train, y_test = cross_validation.train_test_split(X,y,test_size=0.2, random_state=0)
	print y_test
	clf.fit(x_train,y_train)
	y_predicted = clf.predict(x_test)
	
	# precicision:

	cm = confusion_matrix(y_test, y_predicted)
	print cm
	tn = cm[0][0]
	fp = cm[0][1]
	tp = cm[1][1]
	fn = cm[1][0]
	print str(tn) + "\t" + str(fp) + "\t" + str(fn) + "\t" + str(tp)
	print float((cm[0][0] + cm[1][1]))/float(len(y_test))

	#p1 = 


	recall = float(tp)/float(tp+fn)
	print recall
	f1 = 2/(1/precision+1/recall)
	print f1
# write it by yourself and calculate precision, recall, f1 and kappa
# five fold 
# significant test
'''