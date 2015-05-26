# User Preference Predicting 

## 文件分为三个部分：Parser, Extract, Predictor

###Parser 用来解析页面，返回一个Result的list，表示所有页面的解析结果，这个list中的元素也是一个list，是SearchResult的list，这是我们自定义的一个Class， 表示一个doc. 

文件分为BaiduParser 和 SogouParser.py

输入为
if __name__=='__main__':
	l = ParseSogou()
	resultlist  = l.getResults(1,3,10,"../Files/query_id.txt","../Sogou/")

其中 1，3 表示 query 列表中的 start&end 索引号（第一个从1开始）
1,3表示1，2（不包括30
10 代表windows， 计算top10 为止。

后面是两个路径， query_file & page_folder 

SearchResult 中包含的变量有
qid: query号
vertical： int类型，记录当前结果是否是垂直搜索
figure：Int类型，记录当前结果是否包含图片