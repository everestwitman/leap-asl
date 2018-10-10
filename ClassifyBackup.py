import numpy as np
import pickle
from sklearn import neighbors, datasets

# Read data sets from file
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
            for k in range(0, 2):
                for m in range(0, 3):
                    X[i, n] = set1[j, k, m, i]
                    X[i + 1000, n] = set2[j, k, m, i]        
                    n = n + 1
                    
    y[0 : 999] = [4] * 1000;
    y[1000 : 1999] = [5] * 1000;
    
    return X, y

def ReduceData(X):
    # Remove middle two joints from fingers
    X = np.delete(X, 1, 1)
    X = np.delete(X, 1, 1)
    # Remove joint bases
    X = np.delete(X, 0, 2)
    X = np.delete(X, 0, 2)
    X = np.delete(X, 0, 2)
    return X
    
def CenterData(X):
    # Center X coordinates
    allXCoordinates = X[:, :, 0, :]
    meanXValue = allXCoordinates.mean()
    X[:, :, 0, :] = allXCoordinates - meanXValue
    
    # Center Y coordinates
    allYCoordinates = X[:, :, 1, :]
    meanYValue = allYCoordinates.mean()
    X[:, :, 1, :] = allYCoordinates - meanYValue
    
    # Center Z coordinates
    allYCoordinates = X[:, :, 2, :]
    meanZValue = allYCoordinates.mean()
    X[:, :, 2, :] = allYCoordinates - meanZValue
    
    return X

# Reduce data 
train4 = ReduceData(train4)
train5 = ReduceData(train5)
test4 = ReduceData(test4)
test5 = ReduceData(test5)

# Center data 
train4 = CenterData(train4)
train5 = CenterData(train5)
test4 = CenterData(test4)
test5 = CenterData(test5)

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
print (numCorrect / 2000.0) * 100
