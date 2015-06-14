import jieba

class text:

	def Coverage(self,text,query): # calculating coverage between text & query
		query = unicode(query,'utf8') 
		q_l = len(query)
		count = 0
		for char in query:
			if char in text:
				count += 1
		score = float(count)/float(q_l)
		return score

	def Similarity(self,text,query): # calculating similarity between text & query
		try:
			query = unicode(query,'utf8')
		except:
			query = query

		q_l, t_l = 0, 0

		for item in query:
			q_l += 1
		for item in text:
			t_l += 1	

		
		if q_l ==0 or t_l== 0:
			return 1

		count = 0
		if q_l < t_l:
			for char in query:
				if char in text:
					count += 1
		else:
			for char in text:
				if char in query:
					count += 1
		score = float(count)/(float(q_l)+float(t_l)-float(count))
		return score

	def CoverageFeature(self,Results, domain):
		Max = 0.0
		Min = 999
		AVG = 0.0
		query = ""
		for item in Results:
			query = item.query
			if domain == "title":
				score = self.Coverage(item.title, item.query)
			else:
				score = self.Coverage(item.snippet, item.query)
			if score < Min:
				Min = score
			if score > Max:
				Max = score
			AVG += score
		if len(Results)==0:
			AVG =0.0
			#print "result is empty " + query+"\t"+domain
		else:
			AVG = AVG/float(len(Results))
		return [Min,Max,AVG]	

	def SimilarityWordFeature(self,Results, domain):
		Max = 0.0
		Min =999
		AVG = 0.0
		for item in Results:
			if domain == "title":
				#score = self.Similarity(item.title, item.query)
				title_word = jieba.cut(item.title,cut_all=False)
				query_word = jieba.cut(item.query,cut_all=False)
				title_word_list, query_word_list = [],[]
				for item in title_word:
					title_word_list.append(item)
				for item in query_word:
					query_word_list.append(item)
				score = self.Similarity(title_word_list,query_word_list)
				#print score
			else:
				#score = self.Similarity(item.snippet, item.query)
				title_word = jieba.cut(item.snippet,cut_all=False)
				query_word = jieba.cut(item.query,cut_all=False)
				title_word_list, query_word_list = [],[]
				for item in title_word:
					title_word_list.append(item)
				for item in query_word:
					query_word_list.append(item)
				score = self.Similarity(title_word_list,query_word_list)
				#print score
			if score < Min:
				Min = score
			if score > Max:
				Max = score
			AVG += score
		if len(Results)==0:
			AVG =0.0
			#print "result is empty " + domain
		else:
			AVG = AVG/float(len(Results))
		return [Min,Max,AVG]	

	def SimilarityFeature(self,Results, domain):
		Max = 0.0
		Min =999
		AVG = 0.0
		for item in Results:
			if domain == "title":
				score = self.Similarity(item.title, item.query)
				#print score
			else:
				score = self.Similarity(item.snippet, item.query)
				#print score
			if score < Min:
				Min = score
			if score > Max:
				Max = score
			AVG += score
		if len(Results)==0:
			AVG =0.0
			#print "result is empty " + domain
		else:
			AVG = AVG/float(len(Results))
		return [Min,Max,AVG]




	def Length(self,Results, domain):
		Max = 0.0
		Min =999
		AVG = 0.0
		for item in Results:
			if domain == "title":
				length = len(item.title.rstrip().lstrip())
			else:
				length = len(item.snippet.rstrip().lstrip())
			if length < Min:
				Min = length
			if length > Max:
				Max = length
			AVG += length
		if len(Results)==0:
			AVG =0.0
			#print "result is empty " + domain
		else:
			AVG = AVG/float(len(Results))
		return [Min,Max,AVG]

	def textCal(self,Results):
		t_length = self.Length(Results, "title")
		s_length = self.Length(Results, "snippet")
		t_coverage = self.CoverageFeature(Results,"title")
		s_coverage = self.CoverageFeature(Results,"snippet")
		t_word_similarity = self.SimilarityWordFeature(Results,"title")
		s_word_similarity = self.SimilarityWordFeature(Results,"snippet")
		t_similarity = self.SimilarityFeature(Results,"title")
		s_similarity = self.SimilarityFeature(Results,"snippet")
		#return t_length+s_length+t_coverage+s_coverage+t_similarity+s_similarity
		return t_length+s_length + t_word_similarity+s_word_similarity + t_similarity + s_similarity

	def text_comparison(self,r1,r2,windows):  # r1 & r2 is for a page with 10 docs
		text1 = ""
		text2 = ""
		windows = min(len(r1),len(r2),windows)
		for i in range(windows):
			text1 += r1[i].title+r1[i].snippet
			text2 += r2[i].title+r1[i].snippet

		word_left = jieba.cut(text1,cut_all=False)
		word_right = jieba.cut(text2,cut_all=False)
		word1, word2 = [],[]
		for item in word_left:
			word1.append(item)
		for item in word_right:
			word2.append(item)
		return self.Similarity(text1,text2) + self.Similarity(word1,word2)

