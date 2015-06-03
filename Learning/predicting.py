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
			flag = 0
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
		if a1 == 0 and a2 == 0:
			flag = -1
		elif a1 == 1 or a2 == 1:
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
		if a1 == 0 and a2 == 0:
			flag = -1
		elif a1 == -1 or a2 == -1:
			flag = -1
		else:
			flag = 0		
	return flag 

def ground_truth(file_path, prediction_type, judgement):#prediciton Path type with differnce? left_right?,judgement means how to calculate 0,1
	y = []
	result_lines = open(file_path,"r").readlines()
	count = 0
	for line in result_lines:
		count += 1
		#print line
		[qid,a1,a2,a3] = line.replace("\n","").strip().split("\t")
		if prediction_type == "difference" and judgement=="contradiction":
			flag = Judge_difference_contradiction(Convert(a1),Convert(a2),Convert(a3))
			#print line.strip() + "\t" + str(flag)
		elif prediction_type == "difference" and judgement == "vote":
			flag = Judge_difference_vote(Convert(a1),Convert(a2),Convert(a3))
		elif prediction_type == "left_right" and judgement == "vote":
			flag = Judge_left_right_vote(Convert(a1),Convert(a2),Convert(a3))
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

	aspects = [vertical_features,text_features,url_features]
	#aspects = [vertical_features]
	#y = ground_truth("../Result/result.txt","difference","vote")
	y = ground_truth("../Result/result.txt","left_right","vote")
	X = write2X(aspects)

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
	#clf = svm.SVC(kernel='linear', C=1)
	#clf = svm.SVC(C=1.0, kernel='rbf', degree=3, gamma=0.0, coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, random_state=None)
	test = ['precision','recall','f1','roc_auc']
	for item in test:
		scores = cross_validation.cross_val_score(clf,X,y,cv=5,scoring=item)
		#scores = clf.fit(x_train,y_train).score(x_test,y_test)
		print(item+" score is "+str(sum(scores)/5))



