from featureExtractor import Feature, ParseBaidu,ParseSogou
import math
import random
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import cross_validation
from sklearn import svm
import xlrd

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



if __name__ == "__main__":


	baidu_parser = ParseBaidu()
	sogou_parser = ParseSogou()
	baidu_lists = baidu_parser.getResults(1,301,10,"../codes/Feature/Files/query_id.txt","../codes/Feature/Baidu/")
	sogou_lists = sogou_parser.getResults(1,301,10,"../codes/Feature/Files/query_id.txt","../codes/Feature/Sogou/")

	feature_calculator = Feature()
	feature_calculator.featuresExtractor(baidu_lists,sogou_lists,"./query.txt")

	X = []
	y = ground_truth("./Result/result.txt","difference","contradiction")

	text_features = feature_calculator.text_features
	query_features = feature_calculator.query_features
	vertical_features = feature_calculator.vertical_features

	for i in range(len(text_features)):
		X.append(text_features[i]+query_features[i]+vertical_features[i])
	print "We got X for " + str(len(X)) +" and Y for " + str(len(y))

	clear_trainning_set(X,y)

	#clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.05,max_depth=3,random_state=0)
	clf = svm.SVC(kernel='linear', C=1)
	test = ['average_precision','recall','f1','roc_auc']
	for item in test:
		scores = cross_validation.cross_val_score(clf,X,y,cv=3,scoring=item)
		#scores = clf.fit(x_train,y_train).score(x_test,y_test)
		print(item+" score is "+str(sum(scores)/3))

