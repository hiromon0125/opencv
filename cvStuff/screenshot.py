from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionAll
import numpy
from PIL import Image
import os

windowName = 'Desktop'

def findWindowId():
    windowDict = {}
    print('searching window id')

    windowList = CGWindowListCopyWindowInfo(
        kCGWindowListOptionAll, kCGNullWindowID)

    for window in windowList:
        windowOwner = window['kCGWindowOwnerName']
        if windowOwner in windowDict:
            try:
                windowDict[windowOwner].append((window['kCGWindowName'], window['kCGWindowNumber']))
            except:
                pass
        else:
            try:
                windowDict[windowOwner] = [(window['kCGWindowName'], window['kCGWindowNumber'])]
            except:
                pass
    
    for owner in windowDict:
        print(owner)
    owner_chosen = input("choose application:")
    windowList = windowDict[owner_chosen]
    for index,window in enumerate(windowList):
        print(index, window[0])
    window_index = input("choose window:")
    windowId = windowList[int(window_index)][1]
    try:
        imageFileName = 'test-screenshot.png'
        os.system('screencapture -x -l %s %s' % (windowId, imageFileName))
        img = Image.open(imageFileName)
        img = numpy.array(img)
        return windowId
    except TypeError:
        print('Could not find window')
        return

def takeScreenshot(windowId):
    imageFileName = 'test-img.png'
    # -x mutes sound and -l specifies windowId
    os.system('screencapture -x -l %s %s' % (windowId, imageFileName))
    img = Image.open(imageFileName)
    img = numpy.array(img)
    os.remove(imageFileName)
    return img