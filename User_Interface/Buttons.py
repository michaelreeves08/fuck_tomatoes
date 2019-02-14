import cv2

def checkButtons(printer, boxes):
	command = cv2.waitKey(10) & 0xFF
	if command == ord('q'):
		boxes.saveSettings()
		printer.home()
		return True
	elif command == ord('d'):
		enableDots = not enableDots
	elif command == ord('f'):
		printer.sendSerial = not printer.sendSerial
	elif command == ord('h'):
		printer.home()
	elif command == ord('c'):
		printer.callibrate()
	return False