import numpy as np
import pickle
from sklearn import neighbors, datasets

# Read data sets from userData/
train0 = pickle.load(open('userData/train0.dat', 'rb'))
test0 = pickle.load(open('userData/test0.dat', 'rb'))

train1 = pickle.load(open('userData/train1.dat', 'rb'))
test1 = pickle.load(open('userData/test1.dat', 'rb'))

train2 = pickle.load(open('userData/train2.dat', 'rb'))
# test2 = pickle.load(open('userData/test2.dat', 'rb'))
test2 = np.load(open('userData/test2.dat', 'r'))

train3 = pickle.load(open('userData/train3.dat', 'rb'))
# test3 = pickle.load(open('userData/test3.dat', 'rb'))
test3 = np.load(open('userData/test3.dat', 'r'))

train4 = pickle.load(open('userData/train4.dat', 'rb'))
test4 = pickle.load(open('userData/test4.dat', 'rb'))

train5 = pickle.load(open('userData/train5.dat', 'rb'))
test5 = pickle.load(open('userData/test5.dat', 'rb'))

train6 = pickle.load(open('userData/train6.dat', 'rb'))
test6 = pickle.load(open('userData/test6.dat', 'rb'))

# train7 = pickle.load(open('userData/train7.dat', 'rb'))
train7 = np.load(open('userData/train2.dat', 'r'))
# test7 = pickle.load(open('userData/test7.dat', 'rb'))
test7 = np.load(open('userData/test7.dat', 'r'))

# train8 = pickle.load(open('userData/train8.dat', 'rb'))
train8 = np.load(open('userData/train8.dat', 'r'))
# test8 = pickle.load(open('userData/test8.dat', 'rb'))
test8 = np.load(open('userData/test8.dat', 'r'))

train9 = pickle.load(open('userData/train9.dat', 'rb'))
test9 = pickle.load(open('userData/test9.dat', 'rb'))

def ReshapeData(set1, set2, set3, set4, set5, set6):
    X = np.zeros((6000, 5*2*3), dtype='f')
    y = [] * 6000
    for i in range(0, 1000):
        n = 0
        for j in range(0, 5):
            for k in range(0, 2):
                for m in range(0, 3):
                    X[i, n] = set1[j, k, m, i]
                    X[i + 1000, n] = set2[j, k, m, i]   
                    X[i + 2000, n] = set3[j, k, m, i]  
                    X[i + 3000, n] = set4[j, k, m, i]
                    X[i + 4000, n] = set5[j, k, m, i]    
                    X[i + 5000, n] = set5[j, k, m, i]      
                    n = n + 1
    
    # for i in range(0, 9):   
    #     y[i * 1000 : i * 1000 + 999] = [i] * 1000;   
         
    y[0 : 999] = [4] * 1000;
    y[1000 : 1999] = [5] * 1000;
    y[2000 : 2999] = [6] * 1000;
    y[3000 : 3999] = [0] * 1000;
    y[4000 : 4999] = [1] * 1000;
    y[5000 : 5999] = [9] * 1000;
    
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
    allZCoordinates = X[:, :, 2, :]
    meanZValue = allZCoordinates.mean()
    X[:, :, 2, :] = allZCoordinates - meanZValue
    
    return X

# Reduce data 
train4 = ReduceData(train4)
train5 = ReduceData(train5)
test4 = ReduceData(test4)
test5 = ReduceData(test5)
train6 = ReduceData(train6)
test6 = ReduceData(test6)

# Center data 
train4 = CenterData(train4)
train5 = CenterData(train5)
test4 = CenterData(test4)
test5 = CenterData(test5)
train6 = CenterData(train6)
test6 = CenterData(test6)

reshapedTrainData = ReshapeData(train4, train5, train6, train0, train1, train9) 
trainX = reshapedTrainData[0]
trainy = reshapedTrainData[1]
print trainX
print trainy

reshapedTestData = ReshapeData(test4, test5, test6, test0, test1, train9)
testX = reshapedTestData[0]
testy = reshapedTestData[1]
print testX
print testy

print trainX.shape
clf = neighbors.KNeighborsClassifier(15)
clf.fit(trainX, trainy)

numCorrect = 0; 
for i in range(1, 2000):
    prediction = clf.predict([testX[i, :]])
    if prediction == testy[i]:
        numCorrect += 1
print (numCorrect / 2000.0) * 100

pickle.dump(clf, open('userData/classifier.p', 'wb'))
