print __doc__

import random
import pylab as pl
from sklearn import svm, datasets
from sklearn.metrics import confusion_matrix
'''
# import some data to play with
iris = datasets.load_iris()
X = iris.data
y = iris.target
n_samples, n_features = X.shape
p = range(n_samples)
random.seed(0)
random.shuffle(p)
X, y = X[p], y[p]
half = int(n_samples / 2)

# Run classifier
classifier = svm.SVC(kernel='linear')
y_ = classifier.fit(X[:half], y[:half]).predict(X[half:])

# Compute confusion matrix
cm = confusion_matrix(y[half:], y_)

print cm

# Show confusion matrix
pl.matshow(cm)
pl.title('Confusion matrix')
pl.colorbar()
pl.show()	
'''

def f(p,r):
	return (2*p*r)/(p+r)

print f(0.609,0.958)
print f(0.743,0.806)
print f(0.834,0.842)
print f(0.643,0.844)
print f(0.613,0.891)
print f(0.793,0.817)
print f(0.841,0.85)
print f(0.583,0.730)
