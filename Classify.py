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

def ReshapeData(set0, set1, set2, set3, set4, set5, set6, set7, set8, set9):
    X = np.zeros((10000, 5*2*3), dtype='f')
    y = [] * 10000
    for i in range(0, 1000):
        n = 0
        for j in range(0, 5):
            for k in range(0, 2):
                for m in range(0, 3):
                    X[i, n] = set0[j, k, m, i]
                    X[i + 1000, n] = set1[j, k, m, i]   
                    X[i + 2000, n] = set2[j, k, m, i]  
                    X[i + 3000, n] = set3[j, k, m, i]
                    X[i + 4000, n] = set4[j, k, m, i]    
                    X[i + 5000, n] = set5[j, k, m, i]    
                    X[i + 6000, n] = set6[j, k, m, i]    
                    X[i + 7000, n] = set7[j, k, m, i]  
                    X[i + 8000, n] = set8[j, k, m, i]  
                    X[i + 9000, n] = set9[j, k, m, i]  
                    n = n + 1
    
    # for i in range(0, 9):   
    #     y[i * 1000 : i * 1000 + 999] = [i] * 1000;   
    
    y[0 : 999] = [0] * 1000;
    y[1000 : 1999] = [1] * 1000;
    y[2000 : 2999] = [2] * 1000;
    y[3000 : 3999] = [3] * 1000;
    y[4000 : 4999] = [4] * 1000;
    y[5000 : 5999] = [5] * 1000;
    y[6000 : 6999] = [6] * 1000;
    y[7000 : 7999] = [7] * 1000;
    y[8000 : 8999] = [8] * 1000;
    y[9000 : 9999] = [9] * 1000;
    
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
train0 = ReduceData(train0)
test0 = ReduceData(test0)
train1 = ReduceData(train1)
test1 = ReduceData(test1)
train2 = ReduceData(train2)
test2 = ReduceData(test2)
train3 = ReduceData(train3)
test3 = ReduceData(test3) 
train4 = ReduceData(train4)
test4 = ReduceData(test4)
train5 = ReduceData(train5)
test5 = ReduceData(test5)
train6 = ReduceData(train6)
test6 = ReduceData(test6)
train7 = ReduceData(train7)
test7 = ReduceData(test7)
train8 = ReduceData(train8)
test8 = ReduceData(test8)
train9 = ReduceData(train9)
test9 = ReduceData(test9)

# Reduce data
train0 = CenterData(train0)
test0 = CenterData(test0)
train1 = CenterData(train1)
test1 = CenterData(test1)
train2 = CenterData(train2)
test2 = CenterData(test2)
train3 = CenterData(train3)
test3 = CenterData(test3) 
train4 = CenterData(train4)
test4 = CenterData(test4)
train5 = CenterData(train5)
test5 = CenterData(test5)
train6 = CenterData(train6)
test6 = CenterData(test6)
train7 = CenterData(train7)
test7 = CenterData(test7)
train8 = CenterData(train8)
test8 = CenterData(test8)
train9 = CenterData(train9)
test9 = CenterData(test9)

reshapedTrainData = ReshapeData(train0, train1, train2, train3, train4, train5, train6, train7, train8, train9) 
trainX = reshapedTrainData[0]
trainy = reshapedTrainData[1]


reshapedTestData = ReshapeData(test0, test1, test2, test3, test4, test5, test6, test7, test8, test9)
testX = reshapedTestData[0]
testy = reshapedTestData[1]

clf = neighbors.KNeighborsClassifier(15)
clf.fit(trainX, trainy)

numCorrect = 0; 
for i in range(1, 2000):
    prediction = clf.predict([testX[i, :]])
    if prediction == testy[i]:
        numCorrect += 1
print (numCorrect / 2000.0) * 100

pickle.dump(clf, open('userData/classifier.p', 'wb'))
