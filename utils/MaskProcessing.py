import cv2
import numpy as np

def GetColorMask(img, sliders):
    saturationMin = sliders.getMaskSettings().saturationMin

    lowerBound = np.array([0, saturationMin, 1])
    upperBound = np.array([20, 255, 255])

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, lowerBound, upperBound)

def ProcessImageMask(mask, ogImg, sliders):
    _open, _close, _erode, _dilate, _saturationMin = sliders.getMaskSettings().getSettingsTuple()

    maskImg = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((_open, _open)), iterations = 1)
    maskImg = cv2.morphologyEx(maskImg, cv2.MORPH_CLOSE, np.ones((_close, _close)), iterations= 2)
    maskImg = cv2.erode(maskImg, np.ones((_erode, _erode)), iterations = 1)
    maskImg = cv2.dilate(maskImg, np.ones((_dilate, _dilate)), iterations = 1)
    
    maskImg = cv2.bitwise_and(ogImg, ogImg, mask = maskImg)
    maskImg = 255 - maskImg
    return maskImg