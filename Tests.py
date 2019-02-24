import Printer, time, cv2
import numpy as np
from utils import Gcode

params = cv2.SimpleBlobDetector_Params()
 
# Change thresholds
params.minThreshold = 1
params.maxThreshold = 256
 
params.filterByArea = True
params.minArea = 350

params.filterByConvexity = False
params.filterByInertia = False

detector = cv2.SimpleBlobDetector_create(params)

cap = cv2.VideoCapture(0)

openVal = 1
closeVal = 11
erode = 10
dilate = 8

cv2.namedWindow('image')

def nothing(x): pass

cv2.createTrackbar('Open','image',openVal,20,nothing)
cv2.createTrackbar('Close','image',closeVal,40,nothing)
cv2.createTrackbar('Erode','image',erode,30,nothing)
cv2.createTrackbar('Dilate','image',dilate,30,nothing)
cv2.createTrackbar('Saturation','image',170,255,nothing)

while 1:
        
    kernelOpen=np.ones((cv2.getTrackbarPos('Open','image'), cv2.getTrackbarPos('Open','image')))
    kernelClose=np.ones((cv2.getTrackbarPos('Close','image'), cv2.getTrackbarPos('Close','image')))
    kernelErode=np.ones((cv2.getTrackbarPos('Erode','image'), cv2.getTrackbarPos('Erode','image')))
    kernelDilate=np.ones((cv2.getTrackbarPos('Dilate','image'), cv2.getTrackbarPos('Dilate','image')))
    saturationMin = cv2.getTrackbarPos('Saturation','image')

    lowerBound=np.array([0,saturationMin,20])
    upperBound=np.array([20,255,255])

    ret, img = cap.read()

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerBound, upperBound)


    mask=cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen, iterations = 1)
    mask=cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernelClose, iterations= 2)
    mask = cv2.erode(mask, kernelErode, iterations = 1)
    mask = cv2.dilate(mask, kernelDilate, iterations = 1)


    maskImg = cv2.bitwise_and(img,img, mask= mask)
    maskImg = 255 - maskImg
    points = detector.detect(maskImg)
    img = cv2.drawKeypoints(img, points, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imshow('image', maskImg)
    cv2.imshow('wut', img)

    command = cv2.waitKey(10) & 0xFF
    if command == ord('q'):
        break

