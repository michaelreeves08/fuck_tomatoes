import cv2

def drawBox(image, points, color, thickness):
	last_point = points[3]
	for point in points:
		cv2.line(image, last_point, point, color, thickness)
		last_point = point

def drawDots(image, points, size, color, thickness):
	for point in points:
		cv2.circle(image, point, size, color, thickness)
	#Mark TopLeft corner with white dot
	cv2.circle(image,points[0], 2, (255,255,255),-1)

def drawImage(frame, printer):
	drawBox(frame, printer.settings.laser_frame.corners, (255, 255, 255), 1)
	drawDots(frame, printer.settings.laser_frame.corners, 10, (255, 0, 0), -1)
	x,y = printer.settings.laser_frame.getCenter()
	cv2.circle(frame, (int(x), int(y)), 4, (0, 255, 0), 1)
	cx,cy = printer.position
	cv2.putText(frame, str((round(cx),round(cy))), (20, 450), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255))
	if printer.sendSerial:
		cv2.circle(frame, (150, 450), 10, (0, 255, 0), 25)
	else:
		cv2.circle(frame, (150, 450), 10, (0, 0, 255), 25)

