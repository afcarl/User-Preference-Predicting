import re
#coding = utf8
#read_file_list = ["result4.csv","result5.csv","result6.csv","result7.csv","result8.csv","result9.csv","result10.csv
read_file_list = ["result7-1.csv","result7-2.csv","result7-3.csv"]
re_data = re.compile(r'(?<=unit_data:).+?(?=,unit_golden)')
re_result = re.compile(r'(?<=result:).+?(?=,correct)')
data_description = re.compile(r'(?<=question_description:).+?(?=,timestamp)')
re_worker= re.compile(r'(?<=worker_id:).+?(?=,result:)')
write_file = open("result.txt","w")
count = 0
q_dict = {}
answer_list = open("golden_answer.txt","r").readlines()
for i in range(len(answer_list)):
    answer_list[i] = unicode(answer_list[i].replace("\n",""),"utf8")
    print answer_list[i]
#print answer_list[0]


def Judge(item, question):
    #print type(question)
    source = question[1]
    #print source
    score = 0
    for i in range(7):
        if item == answer_list[i]:
            score = i-3
    if source == "s":
        score = score*(-1)
    return score


worker_dict = {}
result_dict = {}

for file_name in read_file_list:
    print file_name
    result_file = open(file_name,"r")
    result_lines = result_file.readlines()

    for line in result_lines:
            count += 1
            result_data = re_result.findall(line)
            unit_data = re_data.findall(line)
            workers = re_worker.findall(line)
            try:
                for worker in workers:
                    worker = worker.strip()
                    if worker_dict.has_key(worker):
                        worker_dict[worker] += 1
                    else:
                        worker_dict[worker] = 1
                    print worker+","

                flag = unit_data[0].split("***")
                question = flag[0] +" v.s. " + flag[2]
                qid = flag[0].replace("b","").replace("s","").strip()
                #print question + "\t" + qid,
                print flag[0] +"\t",
                #write_file.write(qid+"\t")
                for item in unit_data:
                    line = line.replace(item,"")
                description = data_description.findall(line)
                for item in description:
                    line = line.replace(item,"")
                #write_file.write(line)
                scores = ""
                result = re_result.findall(line)
                for item in result:
                    item = item.rstrip().lstrip()
                    print item + "\t",
                    score = Judge(unicode(item,"utf8"),flag[0])
                    #print str(score) + '\t'
                    #print str(score) + "\t",
                    #write_file.write(str(score)+"\t")
                    scores += (str(score) + "\t")
                print scores
                result_dict[int(qid)] = scores # save scores to dict for sorting
                #write_file.write("\n")
            except:
                count = count -1 
                #print "test ?"
sorted_result_dict= sorted(result_dict.iteritems(), key=lambda d:d[0], reverse = False)

for item in sorted_result_dict:
    answers = item[1].split("\t")
    if len(answers)==4:
        scores = answers[0] + '\t' + answers[1] + "\t" + answers[2]
    else:
        scores = answers[0] + '\t' + answers[1] + "\t" + answers[2]
    print str(item[0]) + "\t"+ scores + "\t"
    write_file.write(str(item[0]) + "\t"+ scores +"\n")

print str(len(worker_dict)) + "!!"
       # print len(result_data)
#for item in worker:
#    print item + "\t" + str(worker[item])
