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
        
    def RunForever(self):
        while True:
            frame = self.controller.frame()
            
            while (self.lines): 
                ln = self.lines.pop()
                ln.pop(0).remove()
                del ln
                ln = []
                
            # if at least one hand is in the frame 
            if (frame.hands):
                hand = frame.hands[0]
                for i in range(0, 5): 
                    finger = hand.fingers[i]
                    for j in range(0, 4): 
                        bone = finger.bone(j)
                        boneBase = bone.prev_joint
                        boneTip = bone.next_joint
                        print boneTip

                        xBase = boneBase[0]
                        yBase = boneBase[1]
                        zBase = boneBase[2]
                        xTip = boneTip[0]
                        yTip = boneTip[1]
                        zTip = boneTip[2]
                        
                        self.lines.append(self.ax.plot([-xBase, -xTip], [zBase, zTip], [yBase, yTip], 'r'))
                        
            plt.pause(0.00001)
    
deliverable = Deliverable()
deliverable.RunForever()
