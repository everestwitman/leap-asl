import numpy as np
import matplotlib.pyplot as plt
from sklearn import neighbors, datasets



iris = datasets.load_iris()

trainX = iris.data[::2, 1:3]
trainy = iris.target[::2]

testX = iris.data[1::2, 1:3]
testy = iris.target[1::2]

clf = neighbors.KNeighborsClassifier(15)
clf.fit(trainX, trainy)

actualClass = testy[60]
prediction = clf.predict([testX[60, :]])
print actualClass, prediction 

colors = np.zeros((3, 3), dtype='f')
colors[0, :] = [1, 0.5, 0.5]
colors[1, :] = [0.5, 1, 0.5]
colors[2, :] = [0.5, 0.5, 1]

plt.figure()

x = trainX[:, 0]
y = trainX[:, 1]
# plt.scatter(x, y, c=trainy)
x = testX[:, 0]
y = testX[:, 1]
# plt.scatter(x, y, c=testy)

[numItems, numFeatures] = iris.data.shape
for i in range(0, numItems/2): 
    itemClass = int(trainy[i])
    currColor = colors[itemClass, :]
    plt.scatter(trainX[i, 0], trainX[i, 1], facecolor=currColor, s=50, lw=2)

counter = 0

for i in range(0, numItems/2): 
    itemClass = int(testy[i])
    currColor = colors[itemClass, :]
    prediction = int( clf.predict( [testX[i , :]] ) )
    edgeColor = colors[prediction, :]
    plt.scatter(testX[i, 0], testX[i, 1], facecolor=currColor, s=50, lw=2, edgeColor=edgeColor)
    
    
    if (itemClass == prediction):
        counter = counter + 1

counter  = counter * 100.0 / len(testy)
print counter

plt.show()
