os_system = "MacOs"

try:
    # Using Quartz for MacOS
    from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionAll
except:
    # Using pyautogui for everything else
    print("Download Quartz if you are a mac user")
    import win32gui, win32com.client
    import pyautogui
    os_system = "other"
import numpy
from PIL import Image
import os

windowName = 'Desktop'

def findWindowTitle():
    for index,x in enumerate(pyautogui.getAllWindows()):  
        print(index, x.title)
    windowIndex = int(input("choose window by index:"))
    return pyautogui.getAllWindows()[windowIndex].title


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
        image_file_name = 'test-screenshot.png'
        os.system('screencapture -x -l %s %s' % (windowId, image_file_name))
        img = Image.open(image_file_name)
        img = numpy.array(img)
        return windowId
    except TypeError:
        print('Could not find window')
        return

def takeScreenshot(window_id):
    imageFileName = 'test-img.png'
    # -x mutes sound and -l specifies windowId
    os.system('screencapture -x -l %s %s' % (window_id, imageFileName))
    img = Image.open(imageFileName)
    img = numpy.array(img)
    os.remove(imageFileName)
    return img

def takeScreenshotWindows(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)
        x, y, x1, y1 = win32gui.GetClientRect(hwnd)
        x, y = win32gui.ClientToScreen(hwnd, (x, y))
        x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
        im = pyautogui.screenshot(region=(x, y, x1, y1))
        return numpy.array(im)
    else:
        print('Window not found!')