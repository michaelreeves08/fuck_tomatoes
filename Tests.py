import Printer, time, cv2
import numpy as np
from utils import Gcode, Detector, MaskProcessing
from User_Interface import Sliders

cap = cv2.VideoCapture(0)
detector = Detector.InitializeBlobDetector()
cv2.namedWindow('image')
sliders = Sliders.Sliders('image')
printer = Printer.Printer('COM4', (200, 200))

while 1:
    ret, img = cap.read()

    colorMask = MaskProcessing.GetColorMask(img, sliders)
    res = MaskProcessing.ProcessImageMask(colorMask, img, sliders)

    keyPoints = detector.detect(res)
    img = cv2.drawKeypoints(img, keyPoints, np.array([]), (255, 0, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    if keyPoints:
        points = [xy.pt for xy in keyPoints]
        printer.sendPackage(points)


    # print('-------PACKAGE COUNT: %d-------'%(len(points)))
    # print(Gcode.buildGcodePackage(points, printer, False))

    cv2.imshow('image', res)
    cv2.imshow('color', colorMask)
    cv2.imshow('cum', img)

    command = cv2.waitKey(10) & 0xFF
    if command == ord('q'): break