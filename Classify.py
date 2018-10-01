import numpy as np
import pickle
from sklearn import neighbors, datasets

f = open('userData/train4.dat', 'rb')
train4 = pickle.load(f)

f = open('userData/train5.dat', 'rb')
train5 = pickle.load(f)

f = open('userData/test4.dat', 'rb')
test4 = pickle.load(f)

f = open('userData/test5.dat', 'rb')
test5 = pickle.load(f)

print train4.shape
print train5.shape
print test4.shape
print test5.shape

def ReshapeData(set1, set2):
    X = np.zeros((2000, 5*4*6), dtype='f')
    y = [] * 2000
    for i in range(0, 1000):
        n = 0
        for j in range(0, 5):
            for k in range(0, 4):
                for m in range(0, 6):
                    X[i, n] = set1[j, k, m, i]
                    X[i + 1000, n] = set2[j, k, m, i]        
                    n = n + 1
                    
    y[0 : 999] = [4] * 1000;
    y[1000 : 1999] = [5] * 1000;
    
    return X, y

reshapedTrainData = ReshapeData(train4, train5) 
trainX = reshapedTrainData[0]
trainy = reshapedTrainData[1]
print trainX
print trainy

reshapedTestData = ReshapeData(test4, test5)
testX = reshapedTestData[0]
testy = reshapedTestData[1]
print testX
print testy

clf = neighbors.KNeighborsClassifier(15)
clf.fit(trainX, trainy)

numCorrect = 0; 
for i in range(1, 2000):
    prediction = clf.predict([testX[i, :]])
    if prediction == testy[i]:
        numCorrect += 1
print numCorrect / 2000.0 * 100
