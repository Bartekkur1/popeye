from const import *
from windowUtil import *
from PIL import ImageGrab
import cv2
import numpy as np
import time


class Popeye():

    _window = None
    x, y, w, h = [0, 0, 0, 0]
    templates = []

    def __init__(self):
        pass

    def run(self):
        self.setupWindow()
        self.loadTemplates()
        self.watchWindowLoop()
        pass

    def setupWindow(self):
        window = getWindowByTitle(APP_NAME)
        moveWindow(window, RESIZE_WIDTH, RESIZE_HEIGHT)
        moveWindowToForeground(window)
        self.x, self.y, self.w, self.h = getWindowSize(window)
        pass

    # Warning! infinite loop
    def watchWindowLoop(self, preview: bool = False):
        loopStartTime = int(time.time())
        loopPeriod = 0.1
        while True:
            loopTime = time.time()
            if(loopTime > loopStartTime + loopPeriod):
                loopStartTime = loopTime
                rawImage = ImageGrab.grab(bbox=self.getWindowBbox())
                cv2.imshow("Popeye", self.processImage(np.array(rawImage)))
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        pass

    def getWindowBbox(self):
        return (self.x + WIDTH_FIX, self.y + APP_TITLEBAR_HEIGHT, APP_WIDTH + self.x, APP_HEIGHT + self.y)

    def loadTemplates(self):
        for i in range(1, 12):
            print("Loading {} image".format(i))
            self.templates.append(cv2.imread(
                "bobbers/bobber{}.png".format(i), 0))

    def processImage(self, img_rgb):
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        for template in self.templates:
            res = cv2.matchTemplate(
                img_gray, template, cv2.TM_CCOEFF_NORMED)

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            # print(min_val, max_val, min_loc, max_loc)

            bottom_right = (max_loc[0] + 70, max_loc[1] + 70)
            img_rgb = cv2.rectangle(img_rgb, max_loc, bottom_right, 255, 2)
        return img_rgb
