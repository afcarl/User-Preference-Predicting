# User Preference Predicting 

## 文件分为三个部分：Parser, Extract, Predictor
## 另外新加入的压缩包SERPs for S&B.zip是 query,页面，标注结果和文档说明.标注结果中，负数表示倾向baidu，正数表示倾向sogou

###Parser 

用来解析页面，返回一个Result的list，表示所有页面的解析结果，这个list中的元素也是一个list，是SearchResult的list，这是我们自定义的一个Class， 表示一个doc. 

文件分为 **BaiduParser** 和 **SogouParser.py**

输入为
>if __name__=='__main__':
>	l = ParseSogou()
>	resultlist  = l.getResults(1,3,10,"../Files/query_id.txt","../Sogou/")

其中 1，3 表示 query 列表中的 start&end 索引号（第一个从1开始）
1,3表示1，2（不包括30
10 代表windows， 计算top10 为止。

后面是两个路径， query_file & page_folder 

SearchResult 中包含的变量有
qid: query号
vertical： int类型，记录当前结果是否是垂直搜索
figure：Int类型，记录当前结果是否包含图片


### Extractor

**featureExtractor.py** 是核心代码，定义了一个类 Feature，希望能返回所有的特征。但是首先分为了 aspect，再看第几条结果。恩，应该说是特征类型有限的分类。

特征的类别：
#####（1）URL：Jaccard&Kendall’s tau （不区分baidu,sogou)
#####（2）vertical : v_first(第一次出现veritical位置的倒数），v_num (出现veritcal结果的数量），f_first, f_num 含义类似，知识把veritcal换成了图片 （区分Baidu,Sogou, 和差值Delta)
#####（3）Query: Type, 长度分为 汉字数量和 利用Jieba分词后的词语数量
需要输入文件 query_type:
文件格式：
> **query+”\t”+query_type**
需要人工标注

#####（4）Text: for now 有54个features, 从三个角度来看：Sogou, Baidu, Delta. 18又分为 avg, min, max  6个又被分为 snippet,title  3个又被分为 coverage, similarity & length
#####（5）

#### 调用的信息可以如下代码
``` python
feature_calculator = Feature()
feature_calculator.featuresExtractor(baidu_lists,sogou_lists,"./query.txt")
text_features = feature_calculator.text_features
query_features = feature_calculator.query_features
vertical_features = feature_calculator.vertical_features
```
注意到 featureExtractor的的三个参数，***baidu_list***为搜索结果的SearchResult对象 list 的 list ; 同 ***Sogou_list*** ;
./query.txt 是标注query信息的file 


### Predictor

这部分本来只需要一个文件，但是发现每次都提取一次所有feature的效率太低下了。于是决定分成两个部分，一个是**Write2file**, 另一个是 **Learning/predicting.py**。

write2file.py 将创建两个读取html的对象，解析baidu&sogou文件
之后利用Feature类的函数抓取出不同aspect的特征，存到文件中去。

predicting, 这一部分主要是得到 ** X& y**
X 通过文件得到
y 也是通过文件（标注结果），但是这里设计了一个函数获取不同标准的ground truth。

最后用学习算法计算metrics.