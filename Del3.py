# most be imported outside of Deliverable class to avoid SyntaxError  
from Leap import * 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import random 
import globalVariables as gv

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
    
    def HandleBone(self, i, j):
        self.bone = self.finger.bone(j)
        boneBase = self.bone.prev_joint
        boneTip = self.bone.next_joint
        print boneTip

        xBase = boneBase[0]
        yBase = boneBase[1]
        zBase = boneBase[2]
        xTip = boneTip[0]
        yTip = boneTip[1]
        zTip = boneTip[2]
        
        self.lines.append(self.ax.plot([-xBase, -xTip], [zBase, zTip], [yBase, yTip], 'r'))
        
    def HandleFinger(self, i):
        self.finger = self.hand.fingers[i]
        for j in range(0, 4): 
            self.HandleBone(i, j)
            
    def HandleHands(self):
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
