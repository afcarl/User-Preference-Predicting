from BaiduParser import *
class vertical:
	#def __init__():

	def verticalCal(self,Results):
		first = 0.0
		number = 0
		for i in range(len(Results)):
			if Results[i].vertical == 1:
				if first == 0:
					first = 1/float(i+1)
				number = number + 1
		#print str(first) + "\t" + str(number)
		return [first,number]

	def figureCal(self,Results):
		first = 0.0
		number = 0
		for i in range(len(Results)):
			if Results[i].figure == 1:
				if first == 0:
					first = 1/float(i+1)
				number = number + 1
				#print i
		#print str(first) + "\t" + str(number)
		return [first,number]

	def categoryCal(self,Results):
		category_feature = []
		category = ["encyclopedia","download","video","stock","news","forum","experience","reading","gps_map"]
		for item in category:
			first = 0.0
			number = 0
			for i in range(len(Results)):
				if eval("Results[i]."+item):
					if first == 0:
						first = 1/float(i+1)
					number = number + 1
			category_feature += [first,number]

		return category_feature

if __name__=='__main__':
	p = ParseBaidu()
	v = vertical()
	resultlist  = p.getResults(1,4,10,"../../codes/Feature/Files/query_id.txt","../../codes/Feature/Baidu/")
