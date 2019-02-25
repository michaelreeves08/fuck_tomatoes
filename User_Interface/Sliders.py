import cv2
from settings import maskSettings

openVal = 1
closeVal = 11
erode = 10
dilate = 8
saturationMin = 170

class Sliders:

    def nothing(self, x): pass
    def __init__(self, windowName):
        self.maskSettings = maskSettings.MaskSettings()
        cv2.createTrackbar('Open', windowName, self.maskSettings.open, 20, self.nothing)
        cv2.createTrackbar('Close', windowName, self.maskSettings.close, 40, self.nothing)
        cv2.createTrackbar('Erode', windowName, self.maskSettings.erode, 30, self.nothing)
        cv2.createTrackbar('Dilate', windowName, self.maskSettings.dilate, 30, self.nothing)
        cv2.createTrackbar('Saturation', windowName, self.maskSettings.saturationMin, 255, self.nothing)

    def updateMaskSettings(self):
        self.maskSettings.open = cv2.getTrackbarPos('Open', 'image')
        self.maskSettings.close = cv2.getTrackbarPos('Close', 'image')
        self.maskSettings.erode = cv2.getTrackbarPos('Erode', 'image')
        self.maskSettings.dilate = cv2.getTrackbarPos('Dilate', 'image')
        self.maskSettings.saturationMin = cv2.getTrackbarPos('Saturation', 'image')

    def getMaskSettings(self):
        self.updateMaskSettings()
        return self.maskSettings

