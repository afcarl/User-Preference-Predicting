from BaiduParser import ParseBaidu
from SogouParser import ParseSogou
import jieba
from extract_url import url

class Feature():
	url_features = []
	text_features = []
	vertical_features = []
	query_features = []
	diversity_features = []

	def featuresExtractor(self,baidu,sogou): # baidu & sogou is a list of lists
		self.query_features = queryExtractor(baidu,sogou)
		self.url_features = urlExtractor(baidu,sogou)
		self.text_features = textExtractor(baidu,sogou)
		self.vertical_features = verticalExtractor(baidu,sogou)


	def urlExtractor(self,baidu,sogou):
		num = len(baidu)   # num equals to the number of task that finished by users
		url_features = []
		url_parser = url()
		for i in range(num):
			baidu_page = baidu[i] # one single page of baidu
			sogou_page = sogou[i] # one single page of sogou
			doc_num_baidu = len(baidu)
			doc_num_sogou = len(sogou)
			Jaccard = url_parser.urlJaccard(baidu_page,sogou_page) ## Calculating Jaccard
			tau = url_parser.Kendall(baidu_page,sogou_page)			## Calculating Kendall's tau
			print str(Jaccard) + "\	t" + str(tau)
			url_feature = [Jaccard, tau]
			url_features.append(url_feature)
		return url_features

	

#	def queryDict(query_id, query_type):
#	def queryExtractor(self,baidu,sogou):





baidu_parser = ParseBaidu()
sogou_parser = ParseSogou()

baidu_lists = baidu_parser.getResults(1,4,10,"../codes/Feature/Files/query_id.txt","../codes/Feature/Baidu/")
sogou_lists = sogou_parser.getResults(1,4,10,"../codes/Feature/Files/query_id.txt","../codes/Feature/Sogou/")

feature_calculator = Feature()
url_features = feature_calculator.urlExtractor(baidu_lists,sogou_lists)



'''for i in range(len(baidu_lists)):
	baidu =  baidu_lists[i]
	sogou = sogou_lists[i]
	if baidu[0].query != sogou[0].query:
		print baidu[0].query+"\t" +sogou[0].query'''