from Leap import * 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib.cbook as cbook 
import random 
import globalVariables as gv
import pickle
import numpy as np
from sklearn import neighbors, datasets

clf = pickle.load(open('userData/classifier.p', 'rb'))
testData = np.zeros((1, 30), dtype='f')

database = pickle.load(open('userData/database.p', 'rb'))

def saveDatabase():
    global database
    pickle.dump(database, open('userData/database.p', 'wb'))

# user login 
userName = raw_input('Please enter your name: ')
if (userName in database): 
    database[userName]['logins'] = database[userName]['logins'] + 1
    print 'Welcome back, ' + userName + '.'
else: 
    database[userName] = {'logins': 1}
    for i in range(0, 10):
        signDbEntryName = "digit" + str(i) + "attempted"
        database[userName][signDbEntryName] = 0
    
    print 'Welcome, ' + userName + ''

print database
saveDatabase()

userRecord = database[userName]

controller = Controller()
lines = []

signFrames = 0
signFrameLimit = 20

def NewCurrentNumber(): 
    return (random.randint(0, 9))

programState = 0
currentNumber = NewCurrentNumber()
correctSignFrames = 0

matplotlib.interactive(True)
fig = plt.figure(figsize = (8, 6))

ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-300, 300)
ax.set_ylim(-50, 250)
ax.set_zlim(50, 500)
ax.view_init(azim=90)

# Draw all images as invisible
ax2 = fig.add_subplot(144)
ax3 = fig.add_subplot(326)
ax2.axis('off') # clear x- and y-axes
ax3.axis('off') # clear x- and y-axes
extent = (0, 1, 0, 1)

oneNumber = ax3.imshow(plt.imread("images/zero.png"), extent=extent)
handWaveImage = ax2.imshow(plt.imread("images/handWaveImage.png"), extent=extent, visible=False)
zeroSign = ax2.imshow(plt.imread("images/0_sign.png"), extent=extent, visible=False)
oneSign = ax2.imshow(plt.imread("images/1_sign.png"), extent=extent, visible=False)
twoSign = ax2.imshow(plt.imread("images/2_sign.png"), extent=extent, visible=False)
threeSign = ax2.imshow(plt.imread("images/3_sign.png"), extent=extent, visible=False)
fourSign = ax2.imshow(plt.imread("images/4_sign.png"), extent=extent, visible=False)
fiveSign = ax2.imshow(plt.imread("images/5_sign.png"), extent=extent, visible=False)
sixSign = ax2.imshow(plt.imread("images/6_sign.png"), extent=extent, visible=False)
sevenSign = ax2.imshow(plt.imread("images/7_sign.png"), extent=extent, visible=False)
eightSign = ax2.imshow(plt.imread("images/8_sign.png"), extent=extent, visible=False)
nineSign = ax2.imshow(plt.imread("images/9_sign.png"), extent=extent, visible=False)
arrowLeft = ax2.imshow(plt.imread("images/arrow_left.png"), extent=extent, visible=False)
arrowUp = ax2.imshow(plt.imread("images/arrow_up.png"), extent=extent, visible=False)
arrowDown = ax2.imshow(plt.imread("images/arrow_down.png"), extent=extent, visible=False)
arrowRight = ax2.imshow(plt.imread("images/arrow_right.png"), extent=extent, visible=False)
checkmark = ax2.imshow(plt.imread("images/checkmark.png"), extent=extent, visible=False)

currentImage = handWaveImage


# quit by pressing 'q'
def quit(event):
    if event.key == 'q':
        exit()
    return

plt.connect('key_press_event', quit)

def changeProgramState(state):
    global programState
    programState = state

def ChangeImage(newImg):
    global currentImage
    currentImage.set_visible(False)
    newImg.set_visible(True)
    currentImage = newImg

def CenterData(X): 
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

def DrawCurrentNumber():
    global currentNumber, ax2
    
    if currentNumber == 0: 
        ChangeImage(zeroSign)
    if currentNumber == 1: 
        ChangeImage(oneSign)
    if currentNumber == 2: 
        ChangeImage(twoSign)
    if currentNumber == 3: 
        ChangeImage(threeSign)
    if currentNumber == 4: 
        ChangeImage(fourSign)
    if currentNumber == 5: 
        ChangeImage(fiveSign)
    if currentNumber == 6: 
        ChangeImage(sixSign)
    if currentNumber == 7: 
        ChangeImage(sevenSign)
    if currentNumber == 8: 
        ChangeImage(eightSign)
    if currentNumber == 9: 
        ChangeImage(nineSign)
        
def HandOverDevice():
    return (len(frame.hands) > 0)

def HandCentered():
    global hand
    if hand.sphere_center[0] > 100:
        print "not centered"
        ChangeImage(arrowLeft)
        return False
    elif hand.sphere_center[0] < -100:
        ChangeImage(arrowRight)
        print "not centered"
        return False
    elif hand.sphere_center[2] > 100:
        ChangeImage(arrowUp)
        print "not centered"
        return False
    elif hand.sphere_center[2] < -100:
        ChangeImage(arrowDown)
        print "not centered"
        return False 
    else: 
        return True 
    
def HandleState0(): 
    global programState
    if HandOverDevice():
        changeProgramState(1)
        
    print "Waiting for hand"
    
    ChangeImage(handWaveImage)
    
def HandleState1():
    if HandCentered(): 
        changeProgramState(2)
        
    print "Hand is present BUT NOT centered"
    
def HandleState2():
    print "Hand is present and centered"
    global currentNumber, correctSignFrames
    
    if predictedClass == currentNumber: 
        correctSignFrames += 1
        if correctSignFrames >= 10: 
            currentNumber = NewCurrentNumber()
            changeProgramState(3) 
    else: 
        correctSignFrames = 0
    
    DrawCurrentNumber()  
                
def HandleState3():
    print "Correct!"
    ChangeImage(checkmark)
    changeProgramState(1)

while True:
    if programState in (1,2):
        signFrames = signFrames + 1
        if (signFrames == signFrameLimit):
            signDbEntryName = "digit" + str(currentNumber) + "attempted"
            database[userName][signDbEntryName] = database[userName][signDbEntryName] + 1
            saveDatabase()
            currentNumber = NewCurrentNumber()
            signFrames = 0
        
    frame = controller.frame()
    
    while (lines): 
        ln = lines.pop()
        ln.pop(0).remove()
        del ln
        ln = []
        
    # if at least one hand is in the frame 
    if (HandOverDevice()):
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
            
        testData = CenterData(testData)
        predictedClass = clf.predict(testData)
        
        print "predictedClass: " + str(predictedClass)
        
    else: 
        changeProgramState(0)
        
    plt.pause(0.00001)
    
    print ("State: " + str(programState))
    print ("currentNumber: " + str(currentNumber))
    
    if (programState == 0): # waiting for hand
        HandleState0()
        
    elif (programState == 1): # hand present but not centered
        HandleState1()
         
    elif (programState == 2): # hand is present and centered
        HandleState2()
        
    elif (programState == 3): # user correctly signed current number
        HandleState3()
    
    

    
    
    
