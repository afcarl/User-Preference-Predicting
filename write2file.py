from featureExtractor import Feature, ParseBaidu,ParseSogou
import math
import random

import xlrd



def write2file(file_path,features):
	for feature in features:
		for item in feature:
			file_path.write(str(item)+"\t")
		file_path.write("\n")



if __name__ == "__main__":


	baidu_parser = ParseBaidu()
	sogou_parser = ParseSogou()
	baidu_lists = baidu_parser.getResults(1,301,10,"../codes/Feature/Files/query_id.txt","../codes/Feature/Baidu/")
	sogou_lists = sogou_parser.getResults(1,301,10,"../codes/Feature/Files/query_id.txt","../codes/Feature/Sogou/")

	feature_calculator = Feature()
	feature_calculator.featuresExtractor(baidu_lists,sogou_lists,"./query.txt")


	text_features = feature_calculator.text_features
	query_features = feature_calculator.query_features
	vertical_features = feature_calculator.vertical_features
	url_features = feature_calculator.url_features

	text_features_file = open("./Learning/text_features.txt","w")
	query_features_file = open("./Learning/query_features.txt","w")
	vertical_features_file = open("./Learning/vertical_features.txt","w")
	url_features_file = open("./Learning/url_features.txt","w")


	write2file(text_features_file,text_features)
	write2file(vertical_features_file,vertical_features)
	write2file(query_features_file,query_features)
	write2file(url_features_file,url_features)
