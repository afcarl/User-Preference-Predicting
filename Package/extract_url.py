class url:

	def urlSimilar(self,url_a,url_b):
		if url_a =="" or url_b=="":
			return 0
		if url_a in url_b or url_b in url_a:
			return 1
		else:
			return 0

	def cleanurl(self, url1):
		url = url1.replace("http://","").replace("www.","").replace(".com/","").replace(".cn","")
		return url


	def urlJaccard(self, baidu,sogou):
		count = 0
		l_baidu = len(baidu)
		l_sogou = len(sogou)
		if l_baidu==0 or l_sogou==0:
			return 0 
		for i in range(l_baidu):
			for j in range(l_sogou):
				flag = self.urlSimilar(self.cleanurl(baidu[i].url),self.cleanurl(sogou[j].url))
				#if flag:
				#	print cleanurl(baidu[i].url) + "\t" + cleanurl(sogou[j].url)
				if flag > 0:
					count += 1
					break
		#print count
		jaccard = float(count)/float(l_sogou+l_baidu-count)
		return jaccard

	def Kendall(self, baidu,sogou):
		count = 0
		l_baidu = len(baidu)
		l_sogou = len(sogou)
		if l_baidu==0 or l_sogou==0:
			return 0 
		similar_list = []
		for i in range(l_baidu):
			for j in range(l_sogou):
				flag = self.urlSimilar(self.cleanurl(baidu[i].url),self.cleanurl(sogou[j].url))
				if flag:
					if j not in similar_list:
						similar_list.append(j)

		for i in range(len(similar_list)):
			for j in range(i+1,len(similar_list)):
				if similar_list[i]<similar_list[j]:
					count += 1
		#print len(similar_list)
		try:
			tau = float(count)*2/float(l_baidu*(l_baidu-1))
		except:
			tau = float(count)

		return tau


