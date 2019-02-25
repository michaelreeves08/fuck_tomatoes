import cv2, sys, Printer, time
from User_Interface import Draw, MouseManager, Buttons

cap = cv2.VideoCapture(0)
cv2.namedWindow('image')
printer = Printer.Printer('COM4', (200, 200))
mouse = MouseManager.MouseManager(printer)

start_time = time.time()

while 1:
	ret, img = cap.read()

	colorMask = MaskProcessing.GetColorMask(img, sliders)
	processedImg = MaskProcessing.ProcessImageMask(colorMask, img, sliders)

	if time.time() - start_time > 8:
		if not printer.packageIsExecuting():
			print('PRINTER HOMED')
			keyPoints = detector.detect(processedImg)
			points = [xy.pt for xy in keyPoints]
			print('-------PACKAGE COUNT: %d-------'%(len(points)))
			print(Gcode.buildGcodePackage(points, (200, 200), False))

	Draw.drawImage(img, printer)
    cv2.imshow('image', processedImg)
    cv2.imshow('color', colorMask)
    cv2.imshow('cum', img)

	#Add sliders to args
	if Buttons.checkButtons(printer): break

cap.release()
cv2.destroyAllWindows()