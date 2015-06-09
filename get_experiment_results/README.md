这个文件夹主要是处理标注平台得到的实验数据

输入文件就是 result*.csv
主力文件是 split_result.py 
在read_file_list = ["result4.csv","result5.csv","result6.csv","result7.csv","result8.csv","result9.csv","result10.csv"]
中加入你需要解析的文件，然后会按照顺序解析。
结果计入一个dict中，重新按照 qid排序后输出。

golden_answer文件是为了将 汉字标注结果转换为数字，这里还考虑了Sogou&Baidu的位置转换。