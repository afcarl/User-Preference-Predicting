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
	#print str(a1) + "\t" + str(a2) + "\t" + str(a3) + "\t" + str(flag)
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

def balance_trainning_set(x,y):
	delete_list = []
	l_x = len(x)
	l_y = len(y)
	if l_x!=l_y:
		print("Error in Tranning set, break!")
	else:
		for i in range(l_y):
			if y[i]== 1 :  #judge as non-relevant
				if i%2==0:
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

def write2X(aspects):
	X = []
	length = len(aspects[0]) ## How many instances 
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

	text_features_5 = get_features("text_features_5.txt")
	text_features = get_features("text_features.txt")
	#print len(text_features[0])
	query_features = get_features("query_features.txt")

	vertical_features_5 = get_features("vertical_features_5.txt")
	vertical_features = get_features("vertical_features.txt")

	position_features = get_features("position_features.txt")
	position_features_5 = get_features("position_features_5.txt")

	url_features_5 = get_features("url_features_5.txt")
	url_features = get_features("url_features.txt")

	
	

	#position_features_sogou = get_features("Sogou_position.txt")
	#position_features_baidu = get_features ("Baidu_position.txt")

	aspects_1 = [position_features_5,vertical_features_5,query_features,text_features_5]
	aspects_2 = [vertical_features_5]
	#aspects = [url_features]
	#y = ground_truth("../Result/result.txt","difference","contradiction",1000)
	y = ground_truth("../Result/result.txt","left_right","vote",1000)
	X = write2X(aspects_1)[:1000]
	clear_trainning_set(X,y)
	#clear_trainning_set(X2,y2)
	#balance_trainning_set(X,y)
	y1 = 0 
	y0 = 0
	for i in range(len(y)):
		if y[i] == 1:
			y1 += 1
		else:
			y0 += 1

	print "We got X for " + str(len(X)) +" and Y for " + str(len(y))
	print "we have " + str(y1) + "for 1 and " + str(y0) + " for 0" 
	clf = GradientBoostingClassifier(n_estimators=47, learning_rate=0.03,max_depth=3,random_state=0)
	test_X = clf.fit_transform(X,y)
	#clf.fit(X,y)
	importances  = clf.feature_importances_
	position_propotion = 0.0 # 0-8
	vertical_propotion = 0.0 # 9-74
	query_propotion  =0.0 #75-77
	text_propotion = 0.0 #78 - last 
	#print "size of importances " + str(len(importances))

	#indices = np.argsort(importances)[::-1]
	#for f in range(10):
	#	print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))
	
	#print len(test_X[0])
	#clf2 = svm.SVC(C=1.0, kernel='rbf', degree=3, gamma=0.0, coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, random_state=None)
	test = ['accuracy','recall_macro','f1_macro','roc_auc']
	#test =  ['accuracy','f1_macro']
	clf2 = GradientBoostingClassifier(n_estimators=47, learning_rate=0.03,max_depth=3,random_state=0)
	#for item in test:
	#	scores = cross_validation.cross_val_score(clf2,X,y,cv=5,scoring=item)
	#	print(item+" score is "+str(sum(scores)/5))
	gap = 77
	start_ = 0
	end_ = len(X)
	y_predict = {}
	y_prob = {}
	number = 0
	count = 0
	for i in range(5):
		start = i*gap
		end = (i+1)*gap
		X_test, y_test = X[start:min(end,end_)],y[start:min(end,end_)]
		X_train = X[start_:start] + X[end:end_]
		y_train  = y[start_:start] + y[end:end_]
		print len(y_test)
		clf2.fit(X_train,y_train)
		temp =  clf2.predict_proba(X_test)
		print len(temp)
		for item in temp:
			if item[0] <= item[1]:
				y_predict[number] = 1
				y_prob[number] = item[1]
			else:
				y_predict[number] = 0
				y_prob[number] = item[0]
			number += 1

	print len(y_prob)
	print len(y_predict)
	for i in range(end_):
		if y_predict[i] == y[i]:
			count += 1
	print float(count)/float(end_)

	sorted_prob_list= sorted(y_prob.iteritems(), key=lambda d:d[1], reverse = True)
	#for item in sorted_prob_list:
	#	print str(item[0]) + "\t" + str(item[1])
	#print y_predict
	count_right = 0
	right_dict = {}
	for i in range(end_):
		key = sorted_prob_list[i][0]
		print str(key) + "\t" + str(y_predict[key]) + "\t" + str(y[key])
		if y_predict[key] == y[key]:
			count_right+=1 
		right_dict[i+1] = count_right
	test_point = [ i*38 for i in range(1,11)]
	for item in test_point:
		print float(right_dict[item])/float(item)





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
	print "roc_auc score is " + str(roc_auc_score(y, y_major))'''
'''
	#transformX = clf.fit_transform(X[:size_X*4/5],y[:size_X*4/5])
	#newx = clf.transform((X,threshold=0.01),y)
	#print len(transformX[0])
	
	#print clf.score(test_X,y)
		
	

	#clf2 = GradientBoostingClassifier(n_estimators=i, learning_rate=0.03,max_depth=3,random_state=0)
		#for item in test:
		#accuracy2 = sum(cross_validation.cross_val_score(clf2,X2,y2,cv=5,scoring="accuracy"))
		#f1_macro2 = sum(cross_validation.cross_val_score(clf2,X2,y2,cv=5,scoring="f1_macro"))
			#scores  = cross_validation.cross_val_score(clf2,X2,y2,cv=5,scoring=item)
			#print(item+" score is "+ str(sum(scores)/5))
		#if accuracy>accuracy2 and f1_macro>f1_macro2:
		#print str(i) + " !!!! " + str(accuracy/5) + "\t" + str(f1_macro/5) + "\t" + str(accuracy2/5) + "\t" + str(f1_macro2/5)  
'''
