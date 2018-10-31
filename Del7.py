from Leap import * 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib.cbook as cbook 
import random 
# import globalVariables as gv
import pickle
import numpy as np
from sklearn import neighbors, datasets

class LeapAsl:
    def __init__(self):
        self.clf = pickle.load(open('userData/classifier.p', 'rb'))
        self.testData = np.zeros((1, 30), dtype='f')

        self.database = pickle.load(open('userData/database.p', 'rb'))
        self.programState = 0
        self.currentNumber = self.NewCurrentNumber()
        self.correctSignFrames = 0
        self.signFrames = 0
        self.signFrameLimit = 20
        
        matplotlib.interactive(True)
        self.fig = plt.figure(figsize = (8, 6))

        self.controller = Controller()
        self.lines = []
        
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(-300, 300)
        self.ax.set_ylim(-50, 250)
        self.ax.set_zlim(50, 500)
        self.ax.view_init(azim=90)
        
        # Draw all images as invisible
        self.ax2 = self.fig.add_subplot(144)
        self.ax3 = self.fig.add_subplot(326)
        self.ax2.axis('off') # clear x- and y-axes
        self.ax3.axis('off') # clear x- and y-axes
        extent = (0, 1, 0, 1)

        self.handWaveImage = self.ax2.imshow(plt.imread("images/handWaveImage.png"), extent=extent, visible=False)
        self.zeroSign = self.ax2.imshow(plt.imread("images/0_sign.png"), extent=extent, visible=False)
        self.oneSign = self.ax2.imshow(plt.imread("images/1_sign.png"), extent=extent, visible=False)
        self.twoSign = self.ax2.imshow(plt.imread("images/2_sign.png"), extent=extent, visible=False)
        self.threeSign = self.ax2.imshow(plt.imread("images/3_sign.png"), extent=extent, visible=False)
        self.fourSign = self.ax2.imshow(plt.imread("images/4_sign.png"), extent=extent, visible=False)
        self.fiveSign = self.ax2.imshow(plt.imread("images/5_sign.png"), extent=extent, visible=False)
        self.sixSign = self.ax2.imshow(plt.imread("images/6_sign.png"), extent=extent, visible=False)
        self.sevenSign = self.ax2.imshow(plt.imread("images/7_sign.png"), extent=extent, visible=False)
        self.eightSign = self.ax2.imshow(plt.imread("images/8_sign.png"), extent=extent, visible=False)
        self.nineSign = self.ax2.imshow(plt.imread("images/9_sign.png"), extent=extent, visible=False)
        self.arrowLeft = self.ax2.imshow(plt.imread("images/arrow_left.png"), extent=extent, visible=False)
        self.arrowUp = self.ax2.imshow(plt.imread("images/arrow_up.png"), extent=extent, visible=False)
        self.arrowDown = self.ax2.imshow(plt.imread("images/arrow_down.png"), extent=extent, visible=False)
        self.arrowRight = self.ax2.imshow(plt.imread("images/arrow_right.png"), extent=extent, visible=False)
        self.checkmark = self.ax2.imshow(plt.imread("images/checkmark.png"), extent=extent, visible=False)

        self.currentImage = self.handWaveImage
        
        # user login 
        self.userName = raw_input('Please enter your name: ')
        if (self.userName in self.database): 
            self.database[self.userName]['logins'] = self.database[self.userName]['logins'] + 1
            print 'Welcome back, ' + self.userName + '.'
        else: 
            self.database[self.userName] = {'logins': 1}
            for i in range(0, 10):
                signDbEntryName = "digit" + str(i) + "attempted"
                self.database[self.userName][signDbEntryName] = 0
        
            print 'Welcome, ' + self.userName + ''

        self.saveDatabase()
        
        self.userRecord = self.database[self.userName]

    def saveDatabase(self):
        pickle.dump(self.database, open('userData/database.p', 'wb'))

    def NewCurrentNumber(self): 
        return (random.randint(0, 9))

    def changeProgramState(self, newState):
        self.programState = newState

    def ChangeImage(self, newImg):
        self.currentImage.set_visible(False)
        newImg.set_visible(True)
        currentImage = newImg

    def CenterData(self, X): 
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

    def DrawCurrentNumber(self):
        if self.currentNumber == 0: 
            ChangeImage(self.zeroSign)
        if self.currentNumber == 1: 
            ChangeImage(self.oneSign)
        if self.currentNumber == 2: 
            ChangeImage(self.twoSign)
        if self.currentNumber == 3: 
            ChangeImage(self.threeSign)
        if self.currentNumber == 4: 
            ChangeImage(self.fourSign)
        if self.currentNumber == 5: 
            ChangeImage(self.fiveSign)
        if self.currentNumber == 6: 
            ChangeImage(self.sixSign)
        if self.currentNumber == 7: 
            ChangeImage(self.sevenSign)
        if self.currentNumber == 8: 
            ChangeImage(self.eightSign)
        if self.currentNumber == 9: 
            ChangeImage(self.nineSign)
            
    def HandOverDevice(self):
        return (len(self.frame.hands) > 0)

    def HandCentered(self):
        if self.hand.sphere_center[0] > 100:
            # print "not centered"
            ChangeImage(self.arrowLeft)
            return False
        elif self.hand.sphere_center[0] < -100:
            ChangeImage(self.arrowRight)
            # print "not centered"
            return False
        elif self.hand.sphere_center[2] > 100:
            ChangeImage(self.arrowUp)
            # print "not centered"
            return False
        elif self.hand.sphere_center[2] < -100:
            ChangeImage(self.arrowDown)
            # print "not centered"
            return False 
        else: 
            return True 
        
    def HandleState0(self): 
        if self.HandOverDevice():
            self.changeProgramState(1)
            
        # print "Waiting for hand"
        
        self.ChangeImage(self.handWaveImage)
        
    def HandleState1(self):
        if self.HandCentered(): 
            self.changeProgramState(2)
            
        # print "Hand is present BUT NOT centered"
        
    def HandleState2(self):
        # print "Hand is present and centered"
        
        if predictedClass == self.currentNumber: 
            self.correctSignFrames += 1
            if self.correctSignFrames >= 10: 
                cself.currentNumber = NewCurrentNumber()
                changeProgramState(3) 
        else: 
            self.correctSignFrames = 0
        
        DrawCurrentNumber()  
                    
    def HandleState3(self):
        # print "Correct!"
        ChangeImage(self.checkmark)
        changeProgramState(1)
    
    def RunForever(self):
        while True:
            print self.database[self.userName]
            if (self.programState in [1,2]):
                signFrames = signFrames + 1
                if (signFrames == signFrameLimit):
                    signDbEntryName = "digit" + str(currentNumber) + "attempted"
                    
                    self.database[userName][signDbEntryName] = self.database[userName][signDbEntryName] + 1
                    saveDatabase()
                    currentNumber = NewCurrentNumber()
                    signFrames = 0
                        
            self.frame = self.controller.frame()
            
            while (self.lines): 
                ln = lines.pop()
                ln.pop(0).remove()
                del ln
                ln = []
                
            # if at least one hand is in the frame 
            if (self.HandOverDevice()):
                hand = self.frame.hands[0]
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
                        
                        self.lines.append(ax.plot([-xBase, -xTip], [zBase, zTip], [yBase, yTip], 'r'))
                        
                        if ( (j == 0) | (j == 3)):
                            self.testData[0, k] = xTip
                            self.testData[0, k + 1] = yTip
                            self.testData[0, k + 2] = zTip
                            k = k + 3
                    
                self.testData = self.CenterData(testData)
                predictedClass = self.clf.predict(testData)
                
                # print "predictedClass: " + str(predictedClass)
                
            else: 
                self.changeProgramState(0)
                
            plt.pause(0.00001)
            
            # print ("State: " + str(programState))
            # print ("currentNumber: " + str(currentNumber))
            
            if (self.programState == 0): # waiting for hand
                self.HandleState0()
                
            elif (self.programState == 1): # hand present but not centered
                self.HandleState1()
                 
            elif (self.programState == 2): # hand is present and centered
                self.HandleState2()
                
            elif (self.programState == 3): # user correctly signed current number
                self.HandleState3()
    

leapAsl = LeapAsl()
leapAsl.RunForever()



    
    
    
