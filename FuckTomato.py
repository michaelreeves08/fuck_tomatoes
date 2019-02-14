import cv2, sys, Printer
from utils import MatrixConversion
from User_Interface import BoxFrame, Draw, MouseManager

cap = cv2.VideoCapture(1)
ret, frame = cap.read()
cv2.namedWindow('image')

galvo_corners = [(50, 50), (100, 50), (100, 100), (50, 100)]
image_corners = galvo_corners[:]
enableDots = True

laser_frame = BoxFrame.BoxFrame(galvo_corners)
image_frame = BoxFrame.BoxFrame(image_corners)
coeffs = MatrixConversion.find_coeffs(image_corners, galvo_corners)		

printer = Printer.Printer('COM3', coeffs)
printer.begin()

mouse = MouseManager.MouseManager(laser_frame, image_frame, printer)
cv2.setMouseCallback('image', mouse.mouse_event)

while(True):
	ret, frame = cap.read()
	Draw.drawImage(frame, laser_frame, coeffs, printer, enableDots)
	cv2.imshow('image', frame)
	
	command = cv2.waitKey(10) & 0xFF
	if command == ord('q'):
		printer.home()
		break
	elif command == ord('d'):
		enableDots = not enableDots
	elif command == ord('f'):
		printer.sendSerial = not printer.sendSerial
	elif command == ord('h'):
		printer.home()
	elif command == ord('c'):
		printer.callibrate()

cap.release()
cv2.destroyAllWindows()