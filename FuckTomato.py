import cv2, sys, Printer
from User_Interface import Draw, MouseManager, Buttons

cap = cv2.VideoCapture(1)
ret, frame = cap.read()
cv2.namedWindow('image')
printer = Printer.Printer('COM3')
mouse = MouseManager.MouseManager(printer)

while(True):
	ret, frame = cap.read()
	Draw.drawImage(frame, printer)
	cv2.imshow('image', frame)
	if Buttons.checkButtons(printer, printer.settings): break

cap.release()
cv2.destroyAllWindows()