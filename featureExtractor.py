from BaiduParser import ParseBaidu
from SogouParser import ParseSogou
import jieba
from Package.extract_url import url
from Package.extract_vertical import vertical
from Package.extract_text import text

class Feature():
	url_features = []
	text_features = []
	vertical_features = []
	query_features = []
	diversity_features = []
	length = 0

	def Delta(self,feature_a,feature_b):
			delta = []
			numa = len(feature_a)
			numb = len(feature_b)
			if numa != numb:
				print "Bug in Calculating Delta"
			else:
				for i in range(numa):
					delta.append(feature_a[i]-feature_b[i])
				return delta

	def featuresExtractor(self,baidu,sogou,query_type): # baidu & sogou is a list of lists
		self.query_features = self.queryExtractor(baidu,sogou,query_type)
		self.url_features = self.urlExtractor(baidu,sogou)
		self.text_features = self.textExtractor(baidu,sogou)
		self.vertical_features = self.verticalExtractor(baidu,sogou)


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
			#print str(Jaccard) + "\t" + str(tau)
			url_feature = [Jaccard, tau]
			url_features.append(url_feature)
		return url_features

	def verticalExtractor(self,baidu,sogou):
		num = len(baidu)
		vertical_features = []
		vertical_parser = vertical()
		for i in range(num):
			baidu_page = baidu[i]
			sogou_page = sogou[i]
			vertical_feature_baidu = vertical_parser.verticalCal(baidu_page) + vertical_parser.figureCal(baidu_page) + vertical_parser.categoryCal(baidu_page) # codes locates at "./Package/extract_veritcal"
			vertical_feature_sogou = vertical_parser.verticalCal(sogou_page) + vertical_parser.figureCal(sogou_page)
			vertical_feature_delta = self.Delta(vertical_feature_baidu,vertical_feature_sogou)  # calculating delta
			#vertical_feature_delta = []
			vertical_features.append(vertical_feature_baidu+vertical_feature_sogou+vertical_feature_delta)
		return vertical_features

	def number(self,gene):
		count = 0
		for item in gene:
			count += 1
		return count

	def query2int(self,query_type):
		if query_type=="i":
			return 1
		elif query_type=="n":
			return 2
		else:
			return 3
	def queryExtractor(self,baidu,sogou,query_type):
		lines = open(query_type,"r").readlines()
		query_features = []
		for line in lines:
			query = line.split("\t")[0].replace(".html","")
			q_type = self.query2int(line.split("\t")[1].strip())
			query = unicode(query,"utf8")
			char_length = len(query)  ### There still some problem in this one , for number & zimu
			seg_list = jieba.cut(query,cut_all=False)
			word_length = self.number(seg_list)
			
			#print query.encode("utf8")+"\t" + str(char_length) + "\t" + str(word_length) + "\t" + str(q_type)
			query_features.append([char_length,word_length,q_type])
		return query_features

	def textExtractor(self,baidu,sogou):
		num = len(baidu)
		text_features = []
		text_parser = text()
		for i in range(num):
			baidu_page = baidu[i]
			sogou_page = sogou[i]
			text_feature_baidu = text_parser.textCal(baidu_page)
			text_features_sogou = text_parser.textCal(sogou_page)
			text_features_delta = self.Delta(text_feature_baidu,text_features_sogou)
			text_features_comparison = [text_parser.text_comparison(baidu_page,sogou_page,i) for i in range(1,10)]
			#print text_features_comparison

			text_features.append(text_feature_baidu+text_features_sogou+text_features_delta+text_features_comparison)
		#print len(text_features[0])
		return text_features  # dimension 54?


if __name__ == "__main__":
	baidu_parser = ParseBaidu()
	sogou_parser = ParseSogou()

	baidu_lists = baidu_parser.getResults(11,12,10,"../codes/Feature/Files/query_id.txt","../codes/Feature/Baidu/")
	sogou_lists = sogou_parser.getResults(11,12,10,"../codes/Feature/Files/query_id.txt","../codes/Feature/Sogou/")

	feature_calculator = Feature()
	feature_calculator.featuresExtractor(baidu_lists,sogou_lists,"./query.txt")
	text_features = feature_calculator.text_features
	query_features = feature_calculator.query_features
	vertical_features = feature_calculator.vertical_features
	print vertical_features[0]
	url_features= feature_calculator.url_features
	# text_delta_features = 
