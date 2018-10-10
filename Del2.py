from Leap import * 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import random 
import globalVariables as gv
import pickle
import numpy as np
from sklearn import neighbors, datasets

clf = pickle.load(open('userData/classifier.p', 'rb'))
testData = np.zeros((1, 30), dtype='f')

controller = Controller()
lines = []

matplotlib.interactive(True)
fig = plt.figure(figsize = (8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-300, 300)
ax.set_ylim(-50, 250)
ax.set_zlim(50, 500)
ax.view_init(azim=90)

def CenterData(X): 
    print X
    # Center X coordinates
    allXCoordinates = X[0, ::3]
    meanXValue = allXCoordinates.mean()
    X[0, ::3] = allXCoordinates - meanXValue
    
    # Center Y coordinates
    allYCoordinates = X[0, 1::3]
    meanYValue = allYCoordinates.mean()
    X[0, 1::3] = allYCoordinates - meanYValue
    
    # Center Z coordinates
    allZCoordinates = X[0, 2::3]
    meanZValue = allZCoordinates.mean()
    X[0, 2::3] = allZCoordinates - meanZValue
    
    return X

while True:
    frame = controller.frame()
    
    
    while (lines): 
        ln = lines.pop()
        ln.pop(0).remove()
        del ln
        ln = []
        
    # if at least one hand is in the frame 
    if (len(frame.hands) > 0):
        hand = frame.hands[0]
        k = 0
        for i in range(0, 5): 
            finger = hand.fingers[i]
            
            for j in range(0, 4): 
                bone = finger.bone(j)
                boneBase = bone.prev_joint
                boneTip = bone.next_joint

                xBase = boneBase[0]
                yBase = boneBase[1]
                zBase = boneBase[2]
                xTip = boneTip[0]
                yTip = boneTip[1]
                zTip = boneTip[2]
                
                lines.append(ax.plot([-xBase, -xTip], [zBase, zTip], [yBase, yTip], 'r'))
                
                if ( (j == 0) | (j == 3)):
                    testData[0, k] = xTip
                    testData[0, k + 1] = yTip
                    testData[0, k + 2] = zTip
                    k = k + 3
                    
        
        print testData.shape
        print clf
        testData = CenterData(testData)
        predictedClass = clf.predict(testData)
        print predictedClass
    plt.pause(0.00001)
    
    
