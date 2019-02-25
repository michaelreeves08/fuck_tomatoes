import cv2

def InitializeBlobDetector():
    params = cv2.SimpleBlobDetector_Params()
 
    params.minThreshold = 1
    params.maxThreshold = 256
    
    params.filterByArea = True
    params.minArea = 350

    params.filterByConvexity = False
    params.filterByInertia = False

    return cv2.SimpleBlobDetector_create(params)