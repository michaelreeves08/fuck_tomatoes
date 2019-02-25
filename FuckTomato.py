import cv2, sys, Printer, time
from User_Interface import Draw, MouseManager, Buttons

start_time = time.time()

cap = cv2.VideoCapture(0)
cv2.namedWindow('image')
printer = Printer.Printer('COM4', (200, 200))
mouse = MouseManager.MouseManager(printer)

while 1:
	ret, frame = cap.read()
	Draw.drawImage(frame, printer)
	cv2.imshow('image', frame)

	if time.time() - start_time > 8:
		res = printer.packageIsExecuting()
		if not res:
			print(res)
	#if not printer.packageIsExecuting():
		# ...Detection and package send... #
		#After g-code package send, check for XY reset and update printer execution status
		#pass

	if Buttons.checkButtons(printer): break

cap.release()
cv2.destroyAllWindows()