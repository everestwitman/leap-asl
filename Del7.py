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
        
        self.UserLogin()
    
    def UserLogin(self): 
        # user login 
        self.userName = raw_input('Please enter your name: ')
        if (self.userName in self.database): 
            self.database[self.userName]['logins'] = self.database[self.userName]['logins'] + 1
            print 'Welcome back, ' + self.userName + '.'
        else: 
            self.database[self.userName] = {'logins': 1}
            for i in range(0, 10):
                self.database[self.userName]["digit" + str(i) + "attempted"] = 0
                self.database[self.userName]["digit" + str(i) + "answers"] = [0, 0, 0, 0, 0, 0] 
        
            print 'Welcome, ' + self.userName + ''
        self.userRecord = self.database[self.userName]
        self.saveDatabase()
    def saveDatabase(self):
        pickle.dump(self.database, open('userData/database.p', 'wb'))

    def NewCurrentNumber(self): 
        return (random.randint(0, 9))

    def changeProgramState(self, newState):
        self.programState = newState

    def ChangeImage(self, newImg):
        self.currentImage.set_visible(False)
        newImg.set_visible(True)
        self.currentImage = newImg

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
            self.ChangeImage(self.zeroSign)
        if self.currentNumber == 1: 
            self.ChangeImage(self.oneSign)
        if self.currentNumber == 2: 
            self.ChangeImage(self.twoSign)
        if self.currentNumber == 3: 
            self.ChangeImage(self.threeSign)
        if self.currentNumber == 4: 
            self.ChangeImage(self.fourSign)
        if self.currentNumber == 5: 
            self.ChangeImage(self.fiveSign)
        if self.currentNumber == 6: 
            self.ChangeImage(self.sixSign)
        if self.currentNumber == 7: 
            self.ChangeImage(self.sevenSign)
        if self.currentNumber == 8: 
            self.ChangeImage(self.eightSign)
        if self.currentNumber == 9: 
            self.ChangeImage(self.nineSign)
            
    def HandOverDevice(self):
        return (len(self.frame.hands) > 0)

    def HandCentered(self):
        if self.hand.sphere_center[0] > 100:
            # print "not centered"
            self.ChangeImage(self.arrowLeft)
            return False
        elif self.hand.sphere_center[0] < -100:
            self.ChangeImage(self.arrowRight)
            # print "not centered"
            return False
        elif self.hand.sphere_center[2] > 100:
            self.ChangeImage(self.arrowUp)
            # print "not centered"
            return False
        elif self.hand.sphere_center[2] < -100:
            self.ChangeImage(self.arrowDown)
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
        
        self.CycleSigns()
        
        if self.predictedClass == self.currentNumber: 
            self.correctSignFrames += 1
            if self.correctSignFrames >= 10: 
                self.currentNumber = NewCurrentNumber()
                changeProgramState(3) 
                signAnswersDbEntryName = "digit" + str(currentNumber) + "answers"
                self.database[self.userName][signAnswersDbEntryName].append(1) # signed digit correctly
        else: 
            self.correctSignFrames = 0
        
        self.DrawCurrentNumber()  
                    
    def HandleState3(self):
        # print "Correct!"
        self.ChangeImage(self.checkmark)
        self.changeProgramState(1)
        
    def SignFrameLimit(self, digit):
        correctInLastFiveAttempts = 0 
        for x in self.database[self.userName]["digit" + str(digit) + "answers"][-5:]: # signed digit correctly
            if x == 1: 
                correctInLastFiveAttempts += 1
                
        if correctInLastFiveAttempts == 0:        
            return 20
        else: 
            return 20
        
    def CycleSigns(self):
        print self.database[self.userName]
        signFrameLimit = self.SignFrameLimit(self.currentNumber)
        self.signFrames = self.signFrames + 1
        if (self.signFrames == signFrameLimit):
            signDbEntryName = "digit" + str(self.currentNumber) + "attempted"
            self.database[self.userName][signDbEntryName] = self.database[self.userName][signDbEntryName] + 1
            self.database[self.userName]["digit" + str(self.currentNumber) + "answers"].append(0) # failed to sign correctly
            
            self.saveDatabase()
            self.currentNumber = self.NewCurrentNumber()
            self.signFrames = 0

    def RunForever(self):
        while True:
            self.frame = self.controller.frame()
            
            while (self.lines): 
                ln = self.lines.pop()
                ln.pop(0).remove()
                del ln
                ln = []
                
            # if at least one hand is in the frame 
            if (self.HandOverDevice()):
                self.hand = self.frame.hands[0]
                k = 0
                for i in range(0, 5): 
                    finger = self.hand.fingers[i]
                    
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
                        
                        self.lines.append(self.ax.plot([-xBase, -xTip], [zBase, zTip], [yBase, yTip], 'r'))
                        
                        if ( (j == 0) | (j == 3)):
                            self.testData[0, k] = xTip
                            self.testData[0, k + 1] = yTip
                            self.testData[0, k + 2] = zTip
                            k = k + 3
                    
                self.testData = self.CenterData(self.testData)
                self.predictedClass = self.clf.predict(self.testData)
                
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



    
    
    
