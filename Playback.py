import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib

class Reader: 
    def __init__(self):
        fileName = 'userData/numOfGestures.dat'
        f = open(fileName, 'r')
        self.numberOfGesturesSaved = int(f.read())
        f.close()
        
        matplotlib.interactive(True)
        
        self.lines = []
        self.fig = plt.figure(figsize = (8, 6))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(-300, 300)
        self.ax.set_ylim(-50, 250)
        self.ax.set_zlim(50, 500)
        self.ax.view_init(azim=90)
        
    def PrintGesture(self, i):
        fileName = "userData/gesture%i.dat" % (i)
        f = open(fileName, 'r')
        gestureData = np.load(f)
        f.close()
        
        for i in range(0, 5): 
            for j in range(0, 4): 
                xBase = gestureData[i, j, 0]
                yBase = gestureData[i, j, 1]
                zBase = gestureData[i, j, 2]
                xTip = gestureData[i, j, 3]
                yTip = gestureData[i, j, 4]
                zTip = gestureData[i, j, 5]
                
                print xBase, yBase, zBase, xTip, yTip, zTip
                print self.lines
                self.lines.append(self.ax.plot([-xBase, -xTip], [zBase, zTip], [yBase, yTip], 'b'))
                # self.lines.append(self.ax.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip],'b'))
                plt.pause(0.5)
                
        # delete drawn lines 
        while (self.lines): 
            ln = self.lines.pop()
            ln.pop(0).remove()
            del ln
            ln = []
        
    def PrintData(self):    
        for i in range(0, self.numberOfGesturesSaved + 1):
            self.PrintGesture(i)
            
    def RunForever(self): 
        self.PrintData()
        
reader = Reader()
reader.RunForever()
