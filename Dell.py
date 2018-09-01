from Leap import * 
from pylab import * 
import random 
import globalVariables as gv

controller = Controller()
ion()
show()
# draw a point
xPt = 0 
yPt = 0
pt, = plot(xPt, yPt, 'ko', markersize=20)
# set length of axes
xlim(-100, 100)
ylim(50, 450)

while True:
    frame = controller.frame()
    
    # if at least one hand is in the frame 
    if (len(frame.hands)):
        hand = frame.hands[0]
        fingers = hand.fingers
        indexFinger = fingers.finger_type(Finger.TYPE_INDEX)[0]
        distalPhalanx = indexFinger.bone(Bone.TYPE_DISTAL)
        distalPhalanxPosition = distalPhalanx.next_joint
        print distalPhalanxPosition
        
        x = distalPhalanxPosition[0]
        if (x < gv.xMin):
            gv.xMin = x 
        if (x > gv.xMin): 
            gv.xMax = x
        y = distalPhalanxPosition[1]
        if (y < gv.yMin):
            gv.yMin = y 
        if (y > gv.yMin): 
            gv.yMay = y
        
        print(x)
        print(y)
        
        pt.set_xdata(x)
        pt.set_ydata(y)
    
        pause(0.00001)
    
