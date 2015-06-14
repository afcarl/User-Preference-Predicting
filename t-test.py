import math


def sqrt(a,avg):
	a_sum = 0.0 
	for item in a:
		a_sum += (avg-item)*(avg-item)
	return a_sum



def T_test(a,b):
	a_avg = sum(a)/len(a)
	print a_avg
	b_avg = sum(b)/len(b)
	print b_avg
	sp = (sqrt(a,a_avg) + sqrt(b,b_avg))/float(2*len(a)-2)
	t = (a_avg-b_avg-0)/math.sqrt(2*sp*sp/len(a))

	return t

a = [ 0.76252561  ,0.65077296,  0.59180457,  0.65238095,  0.55145929]
b=[ 0.77203647,0.66666667 ,0.59180457  ,0.64025232,  0.58757062]
print T_test(b,a)

