import Printer, time, cv2
import numpy as np
from utils import Gcode, Detector, MaskProcessing
from User_Interface import Sliders

cap = cv2.VideoCapture(0)

detector = Detector.InitializeBlobDetector()
cv2.namedWindow('image')

sliders = Sliders.Sliders('image')

while 1:
    ret, img = cap.read()

    colorMask = MaskProcessing.GetColorMask(img, sliders)
    res = MaskProcessing.ProcessImageMask(colorMask, img, sliders)

    points = detector.detect(res)
    img = cv2.drawKeypoints(img, points, np.array([]), (255, 0, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imshow('image', res)
    cv2.imshow('cum', img)
    cv2.imshow('color', colorMask)

    command = cv2.waitKey(10) & 0xFF
    if command == ord('q'):
        break

