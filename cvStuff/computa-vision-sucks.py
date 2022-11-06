import numpy as np
import cv2
import screenshot


def onTrack1(val):
    global hueLow
    hueLow=val
    print('Hue Low',hueLow)
def onTrack2(val):
    global hueHigh
    hueHigh=val
    print('Hue High',hueHigh)
def onTrack3(val):
    global satLow
    satLow=val
    print('Sat Low',satLow)
def onTrack4(val):
    global satHigh
    satHigh=val
    print('Sat High',satHigh)
def onTrack5(val):
    global valLow
    valLow=val
    print('Val Low',valLow)
def onTrack6(val):
    global valHigh
    valHigh=val
    print('Val High',valHigh)

width=500
height=300
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 60)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

cv2.namedWindow('myTracker')
cv2.moveWindow('myTracker',width,0)
"""
to detect a blue ball
Hue Low 118
Hue High 121
Sat low 206
sat high 255
val low 140
val high 255
"""
hueLow=118
hueHigh=200
satLow=142
satHigh=255
valLow=140
valHigh=255

cv2.createTrackbar('Hue Low','myTracker',hueLow,179,onTrack1)
cv2.createTrackbar('Hue High','myTracker',hueHigh,179,onTrack2)
cv2.createTrackbar('Sat Low','myTracker',satLow,255,onTrack3)
cv2.createTrackbar('Sat High','myTracker',satHigh,255,onTrack4)
cv2.createTrackbar('Val Low','myTracker',valLow,255,onTrack5)
cv2.createTrackbar('Val High','myTracker',valHigh,255,onTrack6)

windowId = None
windowTitle = None
last_circles = [None for _ in range(3)]

ignore,  frame = cam.read()
if frame is not None:
    image_system_choice = input("Use webcam? (y/n):")
    if image_system_choice.lower() == "y":
        image_system = "webcam"
    else:
        image_system = "screenshot"
        windowTitle = screenshot.findWindowTitle()
else:
    image_system = "screenshot"
    windowId = screenshot.findWindowId()

while True:
    if windowTitle is None and windowTitle is None:
        ignore,  frame = cam.read()
    elif windowTitle is None:
        frame=screenshot.takeScreenshot(windowId)
    else:
        frame=screenshot.takeScreenshotWindows(windowTitle)
    frameHSV=cv2.cvtColor(frame,cv2.COLOR_RGB2HSV)
    lowerBound=np.array([hueLow,satLow,valLow])
    upperBound=np.array([hueHigh,satHigh,valHigh])
    myMask=cv2.inRange(frameHSV,lowerBound,upperBound)
    #myMask=cv2.bitwise_not(myMask)
    myMask = cv2.blur(myMask, (3, 3))
    detected_circle = cv2.HoughCircles(myMask, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    myObject=cv2.bitwise_and(frame,frame,mask=myMask)
    if detected_circle is not None:
        # Convert the circle parameters a, b and r to integers.
        detected_circle = np.uint16(np.around(detected_circle))
        for pt in detected_circle[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            last_circles.insert(0,(a, b))
            last_circles.pop()
            # Draw the circumference of the circle.
            cv2.circle(myObject, (a, b), r, (0, 255, 0), 2)
            if last_circles[0] is not None and last_circles[-1] is not None:
                start_line = last_circles[-1]
                end_line = last_circles[0]
                cv2.line(myObject, start_line,end_line, (0, 0, 255), 2)
    myObjectSmall=cv2.resize(myObject,(int(width/2),int(height/2)))
    cv2.imshow('My Object',myObject)
    cv2.moveWindow('My Object',int(width/2),int(height))
    myMaskSmall=cv2.resize(myMask,(int(width/2),int(height/2)))
    cv2.imshow('My Mask',myMask)
    cv2.moveWindow('My Mask',0,height)
    cv2.imshow('My Webcam', frame)
    cv2.moveWindow('My Webcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()