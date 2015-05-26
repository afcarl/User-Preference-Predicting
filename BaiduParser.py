from bs4 import BeautifulSoup
import traceback

def clean_url(url):
	part = url.split("/")
	length = len(part)
	#print length
	if length !="1":
		url = url.replace(part[length-1],"")
	return url

class SearchResult:
	title = ""
	snippet = ""
	url = ""
	query = ""
	qid = 0
	figure = 0
	vertical = 0
	coverage = 0.0
	Similarity = 0.0
	rank = 0

	def __init__(self, qid,  query, rank, title,snippet, url, vertical,figure):
		self.qid = qid
		self.query = query
		self.rank= rank
		self.title = title
		self.snippet = snippet
		self.url = url
		self.vertical = vertical
		self.figure = figure

	def Print(self):
		print str(self.qid)+"\t" + self.query + "\t"+ str(self.rank) + "\t" + self.snippet.encode("utf8") + "\t figure? " + str(self.figure) 

class ParseBaidu:

	def getResults(self,start_a,end_b,windows,query_file_path,page_folder_path):
		# threshold is top t result
		result_list = []
		#queries_lines = open("../Files/query_id.txt","r").readlines()
		queries_lines = open(query_file_path,"r").readlines()
		queries = ["index"] # start from 1
		for query in queries_lines:
			query = query.split("\t")[0]
			queries.append(query)

		for i in range(start_a,end_b):
			#file_path = "../Baidu/"+queries[i]
			file_path = page_folder_path+queries[i]
			print file_path
			query = queries[i]
			soup = BeautifulSoup(open(file_path,"r").read())
			query = query.replace(".html","")
			container_l = soup.find_all("div", id = "content_left")[0]
			count = 0
			Results = []
			flag = 0

			for child in container_l.children:
				figure = 0
				count += 1
				try:
					if "result-op" in child["class"]:
						vertical = 1
					else:
						vertical = 0
					img = child.find_all("img")

					if len(img)!=0:
						figure = 1

					title = child.find_all("h3", class_ ="t")[0]			

					if not vertical:
						snippet = 	child.find_all("div", class_ = "c-abstract")[0]
						snippet = snippet.get_text()
						url = child.find_all("div",class_ = "f13")[0]
						url = url.find_all("span",class_ = "g")[0]
						url = clean_url(url.get_text())
					else:
						snippet = ""
						url = child.find_all("span", class_= "c-showurl")[0].get_text()
					result = SearchResult(i,query,count,title.get_text().rstrip().lstrip(),snippet,url,vertical,figure)
					Results.append(result)


				except:
					count = count - 1
					#print "sth is wrong"
					#traceback.print_exc()
				if count > windows:
					print "Windows Ends"
					break
			result_list.append(Results)
		return result_list

if __name__=='__main__':
	p = ParseBaidu()
	resultlist  = p.getResults(1,4,10,"../codes/Feature/Files/query_id.txt","../codes/Feature/Baidu/")
	for result in resultlist:
		for item in result:
			item.Print()