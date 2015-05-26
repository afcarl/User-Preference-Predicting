from baidu_result import ParseBaidu
from sogou_result import ParseSogou

def urlSimilar(url_a,url_b):
	if url_a =="" or url_b=="":
		return 0
	if url_a in url_b or url_b in url_a:
		return 1
	else:
		return 0

def cleanurl(url1):
	url = url1.replace("http://","").replace("www.","").replace(".com/","").replace(".cn","")
	return url


def urlJaccard(baidu,sogou):
	count = 0
	l_baidu = len(baidu)
	l_sogou = len(sogou)
	for i in range(l_baidu):
		for j in range(l_sogou):
			flag = urlSimilar(cleanurl(baidu[i].url),cleanurl(sogou[j].url))
			#if flag:
			#	print cleanurl(baidu[i].url) + "\t" + cleanurl(sogou[j].url)
			if flag > 0:
				count += 1
				break
	print count
	jaccard = float(count)/float(l_sogou+l_baidu-count)
	return jaccard

def Kendall(baidu,sogou):
	count = 0
	l_baidu = len(baidu)
	l_sogou = len(sogou)
	similar_list = []
	for i in range(l_baidu):
		for j in range(l_sogou):
			flag = urlSimilar(cleanurl(baidu[i].url),cleanurl(sogou[j].url))
			if flag:
				if j not in similar_list:
					similar_list.append(j)

	for i in range(len(similar_list)):
		for j in range(i+1,len(similar_list)):
			if similar_list[i]<similar_list[j]:
				count += 1
	print len(similar_list)
	tau = float(count)*2/float(l_baidu*(l_baidu-1))
	return tau




baidu_parser = ParseBaidu()
sogou_parser = ParseSogou()

baidu_lists = baidu_parser.getResults(1,301,10)
sogou_lists = sogou_parser.getResults(1,301,10)


num = len(baidu_lists)
write_file = open("url_features.txt","w")
for i in range(num):
	baidu = baidu_lists[i]
	sogou = sogou_lists[i]
	l_baidu = len(baidu)
	l_sogou = len(sogou)
	Jaccard = urlJaccard(baidu,sogou)
	tau = Kendall(baidu,sogou)
	print str(Jaccard) + "\t" + str(tau)
	write_file.write(str(Jaccard) + "\t" + str(tau)+"\n")