from Leap import * 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib.cbook as cbook 
import random 
import pickle
import numpy as np
from sklearn import neighbors, datasets

class LeapAsl:
    def __init__(self):
        self.database = pickle.load(open('userData/database.p', 'rb'))
        self.UserLogin()
        
        self.clf = pickle.load(open('userData/classifier.p', 'rb'))
        self.testData = np.zeros((1, 30), dtype='f')

        self.programState = 0
        
        self.currentDigitSequenceLength = 2
        self.NewCurrentDigitSequence()
        
        self.correctSignFrames = 0
        self.signFrames = 0
        
        matplotlib.interactive(True)
        self.fig = plt.figure(figsize = (12, 8))

        self.controller = Controller()
        self.lines = []
        
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(-300, 300)
        self.ax.set_ylim(-50, 250)
        self.ax.set_zlim(50, 500)
        self.ax.view_init(azim=90)

        self.ax2 = self.fig.add_subplot(6,6,1)
        self.ax2.axis('off') # clear x- and y-axes
        self.ax3 = self.fig.add_subplot(6,6,2)
        self.ax3.axis('off') # clear x- and y-axes
        self.ax4 = self.fig.add_subplot(6,6,3)
        self.ax4.axis('off') # clear x- and y-axes
        self.ax5 = self.fig.add_subplot(6,6,4)
        self.ax5.axis('off') # clear x- and y-axes
        
        self.LoadImages()
        
    def LoadImages(self):
        extent = (0, 1, 0, 1)
        
        # Draw all images as invisible
        self.checkmark = self.ax4.imshow(plt.imread("images/checkmark.png"), extent=extent, visible=False)
        self.cross = self.ax4.imshow(plt.imread("images/cross.png"), extent=extent, visible=False)
        
        self.arrowLeft = self.ax5.imshow(plt.imread("images/arrow_left.png"), extent=extent, visible=True)
        self.arrowUp = self.ax5.imshow(plt.imread("images/arrow_up.png"), extent=extent, visible=False)
        self.arrowDown = self.ax5.imshow(plt.imread("images/arrow_down.png"), extent=extent, visible=False)
        self.arrowRight = self.ax5.imshow(plt.imread("images/arrow_right.png"), extent=extent, visible=False)  
        self.handWaveImage = self.ax5.imshow(plt.imread("images/handWaveImage.png"), extent=extent, visible=False)  
        
        self.zeroDigit = self.ax3.imshow(plt.imread("images/zero.png"), extent=extent, visible=False)
        self.oneDigit = self.ax3.imshow(plt.imread("images/one.png"), extent=extent, visible=False)
        self.twoDigit = self.ax3.imshow(plt.imread("images/two.png"), extent=extent, visible=False)
        self.threeDigit = self.ax3.imshow(plt.imread("images/three.png"), extent=extent, visible=False)
        self.fourDigit = self.ax3.imshow(plt.imread("images/four.png"), extent=extent, visible=False)
        self.fiveDigit = self.ax3.imshow(plt.imread("images/five.png"), extent=extent, visible=False)
        self.sixDigit = self.ax3.imshow(plt.imread("images/six.png"), extent=extent, visible=False)
        self.sevenDigit = self.ax3.imshow(plt.imread("images/seven.png"), extent=extent, visible=False)
        self.eightDigit = self.ax3.imshow(plt.imread("images/eight.png"), extent=extent, visible=False)
        self.nineDigit = self.ax3.imshow(plt.imread("images/nine.png"), extent=extent, visible=False)
        
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
    
        self.currentImageAx2 = self.zeroSign
        self.currentImageAx3 = self.zeroDigit
        self.currentImageAx4 = self.handWaveImage
        
    def UserLogin(self): 
        # user login 
        self.userName = raw_input('Please enter your name: ')
        if (self.userName in self.database): 
            self.database[self.userName]['logins'] = self.database[self.userName]['logins'] + 1
            print 'Welcome back, ' + self.userName + '.'
        else: 
            self.database[self.userName] = {'logins': 1, 'aggregateAnswers': []}
            for i in range(0, 10):
                self.database[self.userName]["digit" + str(i) + "attempted"] = 0
                self.database[self.userName]["digit" + str(i) + "answers"] = []
        
            print 'Welcome, ' + self.userName + ''
        self.userRecord = self.database[self.userName]
        self.SaveDatabase()
        
    def SaveDatabase(self):
        pickle.dump(self.database, open('userData/database.p', 'wb'))

    def NewCurrentNumber(self): 
        # By ratio right for digit, min one
        # add spaced repetition?
        
        digitDistribution = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(10):
            digitDistribution[i] = 5 - (self.CorrectLastFiveAttempts(i) - 1)
        # print digitDistribution
        
        digitDistributionFlattened = []
        for i in range(len(digitDistribution)):
            for j in range(digitDistribution[i]):
                digitDistributionFlattened.append(i)
        # print digitDistributionFlattened
        
        return random.choice(digitDistributionFlattened)

    def NewCurrentDigitSequence(self):
        if self.LastAggregateAttempt() == 1: 
            self.currentDigitSequenceLength = self.currentDigitSequenceLength + 1
        elif self.currentDigitSequenceLength > 1: 
            self.currentDigitSequenceLength = self.currentDigitSequenceLength - 1
        
        self.currentDigitIndex = 0
        
        self.currentDigitSequence = []
        for x in range(self.currentDigitSequenceLength):
            self.currentDigitSequence.append(self.NewCurrentNumber())
            
        self.currentNumber = self.currentDigitSequence[self.currentDigitIndex]
        
    def ChangeProgramState(self, newState):
        self.programState = newState

    def ChangeImageAx2(self, newImg):
        self.currentImageAx2.set_visible(False)
        newImg.set_visible(True)
        self.currentImageAx2 = newImg

    def ChangeImageAx3(self, newImg):
        self.currentImageAx3.set_visible(False)
        newImg.set_visible(True)
        self.currentImageAx3 = newImg
    
    def ChangeImageAx4(self, newImg):
        self.currentImageAx4.set_visible(False)
        newImg.set_visible(True)
        self.currentImageAx4 = newImg
    
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
    
    def DisplaySign(self, digit):
        return (self.CorrectLastFiveAttempts(digit) < 1)

    def DrawCurrentNumber(self):
        if self.currentNumber == 0: 
            if self.DisplaySign(self.currentNumber): 
                self.ChangeImageAx2(self.zeroSign)
            else: 
                self.currentImageAx2.set_visible(False)
            self.ChangeImageAx3(self.zeroDigit)
        if self.currentNumber == 1: 
            if self.DisplaySign(self.currentNumber): 
                self.ChangeImageAx2(self.oneSign)
            else: 
                self.currentImageAx2.set_visible(False)
            self.ChangeImageAx3(self.oneDigit)
        if self.currentNumber == 2: 
            if self.DisplaySign(self.currentNumber): 
                self.ChangeImageAx2(self.twoSign)
            else: 
                self.currentImageAx2.set_visible(False)
        if self.currentNumber == 3: 
            if self.DisplaySign(self.currentNumber): 
                self.ChangeImageAx2(self.threeSign)
            else: 
                self.currentImageAx2.set_visible(False)
            self.ChangeImageAx3(self.threeDigit)
        if self.currentNumber == 4: 
            if self.DisplaySign(self.currentNumber): 
                self.ChangeImageAx2(self.fourSign)
            else: 
                self.currentImageAx2.set_visible(False)
            self.ChangeImageAx3(self.fourDigit)
        if self.currentNumber == 5: 
            if self.DisplaySign(self.currentNumber): 
                self.ChangeImageAx2(self.fiveSign)
            else: 
                self.currentImageAx2.set_visible(False)
            self.ChangeImageAx3(self.fiveDigit)
        if self.currentNumber == 6: 
            if self.DisplaySign(self.currentNumber): 
                self.ChangeImageAx2(self.sixSign)
            else: 
                self.currentImageAx2.set_visible(False)
            self.ChangeImageAx3(self.sixDigit)
        if self.currentNumber == 7: 
            if self.DisplaySign(self.currentNumber): 
                self.ChangeImageAx2(self.sevenSign)
            else: 
                self.currentImageAx2.set_visible(False)
            self.ChangeImageAx3(self.sevenDigit)
        if self.currentNumber == 8: 
            if self.DisplaySign(self.currentNumber): 
                self.ChangeImageAx2(self.eightSign)
            else: 
                self.currentImageAx2.set_visible(False)
            self.ChangeImageAx3(self.eightDigit)
        if self.currentNumber == 9: 
            if self.DisplaySign(self.currentNumber): 
                self.ChangeImageAx2(self.nineSign)
            else: 
                self.currentImageAx2.set_visible(False)
            self.ChangeImageAx3(self.nineDigit)
            
    def HandOverDevice(self):
        return (len(self.frame.hands) > 0)

    def HandCentered(self):
        if self.hand.sphere_center[0] > 100:
            # print "not centered"
            self.ChangeImageAx2(self.arrowLeft)
            return False
        elif self.hand.sphere_center[0] < -100:
            self.ChangeImageAx2(self.arrowRight)
            # print "not centered"
            return False
        elif self.hand.sphere_center[2] > 100:
            self.ChangeImageAx2(self.arrowUp)
            # print "not centered"
            return False
        elif self.hand.sphere_center[2] < -100:
            self.ChangeImageAx2(self.arrowDown)
            # print "not centered"
            return False 
        else: 
            return True 
        
    def HandleState0(self): 
        if self.HandOverDevice():
            self.ChangeProgramState(1)
            
        # print "Waiting for hand"
        
        self.ChangeImageAx2(self.handWaveImage)
        
        
    def HandleState1(self):
        if self.HandCentered(): 
            self.ChangeProgramState(2)
            
        # print "Hand is present BUT NOT centered"
        
    def HandleState2(self):
        # print "Hand is present and centered"
        self.SignedCorrectly()
        
        self.DrawCurrentNumber()  
        self.SaveDatabase()
                    
    def HandleState3(self):
        # print "Correct!"
        self.ChangeImageAx4(self.checkmark)
        # self.currentImageAx3.set_visible(False)
        
        self.ChangeProgramState(1)
    
    def LastAggregateAttempt(self):
        try: 
            return self.database[self.userName]["aggregateAnswers"][-1]
        except IndexError:
            return 0 
        
    def CorrectLastFiveAggregateAttempts(self): 
        correctLastFiveAttempts = 0 
        attempts = self.database[self.userName]["aggregateAnswers"]
        if len(attempts) > 5:
            for x in attempts[-5:]: 
                if x == 1: 
                    correctLastFiveAttempts += 1
        else: 
            for x in attempts:
                if x == 1: 
                    correctLastFiveAttempts += 1
        return correctLastFiveAttempts
        
    def CorrectLastFiveAttempts(self, digit):
        correctLastFiveAttempts = 0 
        attempts = self.database[self.userName]["digit" + str(digit) + "answers"]
        if len(attempts) > 5:
            for x in attempts[-5:]: 
                if x == 1: 
                    correctLastFiveAttempts += 1
        else: 
            for x in attempts:
                if x == 1: 
                    correctLastFiveAttempts += 1
        return correctLastFiveAttempts
                
    def SignFrameLimit(self, digit):
        correctLastFiveAttempts = self.CorrectLastFiveAttempts(digit)
        if correctLastFiveAttempts != 0:
            return (100 - 10 * correctLastFiveAttempts)  
        else: 
            return 100 
    
    def SignedCorrectly(self):
        # print self.database[self.userName]
        signFrameLimit = self.SignFrameLimit(self.currentNumber)
        self.signFrames = self.signFrames + 1
        
        # Failed to correctly sign current digit 
        if (self.signFrames == signFrameLimit):
            signDbEntryName = "digit" + str(self.currentNumber) + "attempted"
            self.database[self.userName][signDbEntryName] = self.database[self.userName][signDbEntryName] + 1 #increment digits attempts count
            self.database[self.userName]["digit" + str(self.currentNumber) + "answers"].append(0) 
            self.database[self.userName]["aggregateAnswers"].append(0) # signed digit correctly
            
            self.SaveDatabase()
            
            self.ChangeImageAx4(self.cross)
            # self.currentImageAx3.set_visible(False)
            
            self.NewCurrentDigitSequence()
            
            self.signFrames = 0
        
        # Correctly signed current digit
        if self.predictedClass == self.currentNumber: 
            self.correctSignFrames += 1
            if self.correctSignFrames >= 10:
                signDbEntryName = "digit" + str(self.currentNumber) + "attempted"
                signAnswersDbEntryName = "digit" + str(self.currentNumber) + "answers"
                self.database[self.userName][signDbEntryName] = self.database[self.userName][signDbEntryName] + 1 #increment digits attempts count
                self.database[self.userName][signAnswersDbEntryName].append(1) # signed digit correctly
                self.database[self.userName]["aggregateAnswers"].append(1) # signed digit correctly
                
                
                
                if self.currentDigitIndex < len(self.currentDigitSequence) - 1: # iterate through digit sequence
                    self.currentDigitIndex = self.currentDigitIndex + 1
                    self.currentNumber = self.currentDigitSequence[self.currentDigitIndex]    
                else: # finish digit sequence
                    self.NewCurrentDigitSequence()
                    
                self.ChangeProgramState(3) 
                
        else: 
            self.correctSignFrames = 0

    def RunForever(self):
        while True:
            print str(self.currentDigitSequence).strip('[]')
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
                self.ChangeProgramState(0)
                
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



    
    
    
