from Leap import * 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import random 
import globalVariables as gv
import numpy as np
import pickle

class Deliverable: 
    def __init__(self):
        matplotlib.interactive(True)
        self.controller = Controller()
        
        self.lines = []
        self.fig = plt.figure(figsize = (8, 6))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(-300, 300)
        self.ax.set_ylim(-50, 250)
        self.ax.set_zlim(50, 500)
        self.ax.view_init(azim=90)
        
        self.previousNumberOfHands = 0 
        self.currentNumberOfHands = 0
        
        self.numberOfGestures = 1000
        self.gestureIndex = 0
        
        self.gestureData = np.zeros((5, 4, 6, self.numberOfGestures), dtype='f')
        self.numberOfGesturesSaved = 0
        
        
    
    def RecordingIsEnding(self):
        return (self.previousNumberOfHands==2) & (self.currentNumberOfHands==1)
        
    def HandleBone(self, i, j):
        self.bone = self.finger.bone(j)
        boneBase = self.bone.prev_joint
        boneTip = self.bone.next_joint

        xBase = boneBase[0]
        yBase = boneBase[1]
        zBase = boneBase[2]
        xTip = boneTip[0]
        yTip = boneTip[1]
        zTip = boneTip[2]
        
        if (self.currentNumberOfHands == 1):
            self.lines.append(self.ax.plot([-xBase, -xTip], [zBase, zTip], [yBase, yTip], 'r', color = 'g'))
        else: 
            self.lines.append(self.ax.plot([-xBase, -xTip], [zBase, zTip], [yBase, yTip], 'r', color = 'r'))
        
        
        if (self.currentNumberOfHands == 2):
            self.gestureData[i, j, 0, self.gestureIndex] = xBase
            self.gestureData[i, j, 1, self.gestureIndex] = yBase
            self.gestureData[i, j, 2, self.gestureIndex] = zBase
            self.gestureData[i, j, 3, self.gestureIndex] = xTip
            self.gestureData[i, j, 4, self.gestureIndex] = yTip
            self.gestureData[i, j, 5, self.gestureIndex] = zTip
            
        
    def HandleFinger(self, i):
        self.finger = self.hand.fingers[i]
        for j in range(0, 4): 
            self.HandleBone(i, j)
            
    def SaveGesture(self):
        fileName = 'userData/gesture.dat'
        f = open(fileName, 'w')
        pickle.dump(self.gestureData, f)
        f.close()
            
    def HandleHands(self):
        self.previousNumberOfHands = self.currentNumberOfHands
        self.currentNumberOfHands = len(self.frame.hands)
         
        self.hand = self.frame.hands[0]
        for i in range(0,5): 
            self.HandleFinger(i)
            
        plt.pause(0.00001)
        
        # delete drawn lines 
        while (self.lines): 
            ln = self.lines.pop()
            ln.pop(0).remove()
            del ln
            ln = []
        
        # if (self.RecordingIsEnding()):
        #     # print self.gestureData[:,:,:]

        
        if (self.currentNumberOfHands == 2): 
            print 'gesture'  + str(self.gestureIndex) + 'stored.'
            self.gestureIndex = self.gestureIndex + 1
            if (self.gestureIndex == self.numberOfGestures): 
                self.SaveGesture()
                # print self.gestureData[:,:,:, 0]
                # print self.gestureData[:,:,:, 99]
                sys.exit(0) 
        
    def RunOnce(self): 
        self.frame = self.controller.frame()
        
        # if at least one hand is in the frame 
        if (self.frame.hands):
            self.HandleHands()
        
    def RunForever(self):
        while True:
            self.RunOnce()
    
deliverable = Deliverable()
deliverable.RunForever()
