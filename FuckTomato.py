import cv2, sys, Printer, time
import numpy as np
from utils import MaskProcessing, Detector, Gcode
from User_Interface import Draw, MouseManager, Buttons, Sliders

cap = cv2.VideoCapture(0)
cv2.namedWindow('image')
printer = Printer.Printer('COM3', (200, 200))
mouse = MouseManager.MouseManager(printer)
sliders = Sliders.Sliders('image')
detector = Detector.InitializeBlobDetector()

start_time = time.time()
buffer_time = time.time()

while 1:
	ret, img = cap.read()

	colorMask = MaskProcessing.GetColorMask(img, sliders)
	processedImg = MaskProcessing.ProcessImageMask(colorMask, img, sliders)

	keyPoints = detector.detect(processedImg)
	img = cv2.drawKeypoints(img, keyPoints, np.array([]), (255, 0, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

	if time.time() - start_time > 8:
		if time.time() - buffer_time > .1:
			if not printer.packageIsExecuting():
				print('PRINTER HOMED')
				points = [xy.pt for xy in keyPoints]
				printer.sendPackage(points)
			buffer_time = time.time()
			

	Draw.drawImage(img, printer)

	cv2.imshow('cum', processedImg)
	cv2.imshow('image', img)
	cv2.imshow('color', colorMask)

	if Buttons.checkButtons(printer, sliders): break

cap.release()
cv2.destroyAllWindows()