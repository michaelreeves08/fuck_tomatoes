import cv2, sys, Printer
from User_Interface import Draw, MouseManager, Buttons

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.namedWindow('image')
printer = Printer.Printer('COM4', (200, 200))
mouse = MouseManager.MouseManager(printer)

while 1:
	ret, frame = cap.read()
	Draw.drawImage(frame, printer)
	cv2.imshow('image', frame)

	print(printer.packageIsExecuting())
	#if not printer.packageIsExecuting():
		# ...Detection and package send... #
		#After g-code package send, check for XY reset and update printer execution status
		#pass

	if Buttons.checkButtons(printer): break

cap.release()
cv2.destroyAllWindows()