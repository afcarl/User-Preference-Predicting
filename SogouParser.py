from bs4 import BeautifulSoup
from SERPExtractor import Parser
class SearchResult:
	title = ""
	snippet = ""
	url = ""
	query = ""
	qid = 0
	vertical = 0.0
	coverage = 0.0
	Similarity = 0.0
	figure = 0
	rank = 0
	
	def __init__(self,qid, query, rank, title,snippet, url, vertical,figure):
		self.qid = qid
		self.query = query
		self.rank = rank
		self.title = title
		self.snippet = snippet
		self.url = url
		self.vertical = vertical
		self.figure = figure

	def Print(self):
		print str(self.qid)+"\t" + self.query + "\t"+ str(self.rank) + "\t" + self.title + "\t figure? " + str(self.figure) 

class ParseSogou:

	def getResults(self,start_a,end_b,windows,query_file_path,page_folder_path):

		result_list = []
		#queries_lines = open("../Files/query_id.txt","r").readlines()
		queries_lines = open(query_file_path,"r").readlines()
		queries = ["index"]
		# start from 1
		for query in queries_lines:
			query = query.split("\t")[0]
			queries.append(query)

		for i in range(start_a,end_b): # the range of query
			#file_path = "../Sogou/"+queries[i]
			file_path = page_folder_path+queries[i]
			query = queries[i].replace(".html","")
			Results = []
			count = 0
			p = Parser()
			resultlists = p.parseSERP(file_path)
			for item in resultlists:
				count += 1

				title = item.title
				url  = item.mainurl
				#print str(item.figure) +"\t" + item.title

				if "title" in item.resulttype:
					#print item.figure
					vertical = 1
				else:
					vertical = 0
				if vertical:
					snippet = item.othertext
				else:
					snippet = item.summary

				result = SearchResult(i,query,count,title,snippet,url,vertical,item.figure)
				Results.append(result)
				if count > windows:
					break
			#print query

			result_list.append(Results)

		return result_list

if __name__=='__main__':
	l = ParseSogou()
	resultlist  = l.getResults(1,3,10,"../codes/Feature/Files/query_id.txt","../codes/Feature/Sogou/")
	for Result in resultlist:
		for item in Result:
			item.Print()
