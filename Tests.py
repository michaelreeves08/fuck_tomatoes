import Printer, time, cv2
import numpy as np
from utils import Gcode

params = cv2.SimpleBlobDetector_Params()
 
# Change thresholds
params.minThreshold = 1
params.maxThreshold = 256
 
# Filter by Area.
params.filterByArea = True
params.minArea = 50

# # Filter by Convexity
# params.filterByConvexity = True
# params.minConvexity = 0.87
 
# # Filter by Inertia
# params.filterByInertia = True
# params.minInertiaRatio = 0.01


detector = cv2.SimpleBlobDetector_create(params)

img = cv2.imread('salad.jpg')
wht = cv2.imread('wht.jpg')
kernelOpen=np.ones((3,3))
kernelClose=np.ones((7,7))
 
lowerBound=np.array([0,180,180])
upperBound=np.array([10,255,255])

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lowerBound, upperBound)
mask=cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen, iterations = 2)
mask=cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernelClose)

maskImg = cv2.bitwise_and(img,img, mask= mask)

maskImg = 255 - maskImg

points = detector.detect(maskImg)

for i in points:
    print i.pt

img = cv2.drawKeypoints(img, points, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imshow('REEE', maskImg)
cv2.imshow('wut', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

