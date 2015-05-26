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