import time
import datetime
import numpy as np
import cv2
from PIL import ImageGrab
from windowUtil import *
from const import *
import pyautogui


class Popeye():

    _window = None
    x, y, w, h = [0, 0, 0, 0]
    bbox = (460, 100, 850, 380)
    rectSize = 15
    bobberPosition = np.array([])
    startTime = time.time()
    catches = 0

    def __init__(self):
        self.bobberPosition = np.array([])
        self.startTime = time.time()

    def defaultMousePosition(self):
        pyautogui.click(990, 720, interval=0.1)

    def startFishing(self):
        pyautogui.press('1', interval=0.1)

    def run(self):
        self.defaultMousePosition()
        self.startFishing()

        self.setupWindow()
        self.watchWindowLoop()

    def setupWindow(self):
        window = getWindowByTitle(APP_NAME)
        moveWindow(window, RESIZE_WIDTH, RESIZE_HEIGHT)
        moveWindowToForeground(window)
        self.x, self.y, self.w, self.h = getWindowSize(window)

    # Warning! infinite loop
    def watchWindowLoop(self, preview: bool = False):
        self.processImage()

    def logCatch(self, timeDiff):
        self.catches += 1
        print("Got'em! catch number: {} | date: {} | fishing time: {}".format(
            self.catches, datetime.datetime.now(), timeDiff))

    def fishCatched(self, x, y):
        if(len(self.bobberPosition) < 5):
            return False

        lastFive = self.bobberPosition[-5:]
        catchValue = np.max(lastFive) + 1
        if(y > catchValue):
            time.sleep(0.5)
            pyautogui.click((x + 450) + 10, (y + 100) + 10,
                            button='right', interval=0.1)
            self.defaultMousePosition()
            return True

    def processImage(self):
        startTime = time.time()
        while True:
            newImage = ImageGrab.grab(bbox=self.bbox)
            hsv = cv2.cvtColor(np.array(newImage), cv2.COLOR_RGB2HSV)

            lower_blue = np.array([50, 68, 68])
            upper_blue = np.array([130, 255, 255])

            mask = cv2.inRange(hsv, lower_blue, upper_blue)

            kernel = np.ones((3, 3), np.uint8)
            dilated = cv2.dilate(mask, kernel, 1)

            contours, hierarchy = cv2.findContours(
                dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

            if(len(contours) > 0):
                x, y, w, h = cv2.boundingRect(contours[-1])
                if(self.fishCatched(x, y)):
                    timeDiff = time.time() - startTime
                    self.logCatch(timeDiff)
                    startTime = time.time()
                    self.bobberPosition = np.array([])
                    time.sleep(1.5)
                    self.defaultMousePosition()
                    self.defaultMousePosition()
                    self.defaultMousePosition()
                    self.startFishing()

                self.bobberPosition = np.append(self.bobberPosition, y)
                newImage = cv2.rectangle(
                    np.array(newImage),
                    (x - self.rectSize, y - self.rectSize),
                    (x + self.rectSize, y + self.rectSize),
                    (0, 0, 255),
                    2)

            cv2.imshow("Popeye", np.array(newImage))
            cv2.imshow("Popeye Dialated", np.array(dilated))

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
