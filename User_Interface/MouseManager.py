import cv2

class MouseManager:
	def __init__(self, printer):
		cv2.setMouseCallback('image', self.mouse_event)
		self.laser_frame = printer.settings.laser_frame
		self.image_frame = printer.settings.image_frame
		self.printer = printer
		self.mouseDrag = False
		self.activeFrame = None

	def mouse_event(self, event, x, y, flags, param):
		if event == cv2.EVENT_LBUTTONDBLCLK:
			pass

		elif event == cv2.EVENT_LBUTTONDOWN:
			self.mouseDrag = True
			self.activeFrame = None
			frames = (self.laser_frame, self.image_frame)
			for frame in frames:
				if frame.isTouching((x, y), 10):
					self.activeFrame = frame
					break
			self.printer.write((x, y))

		elif event == cv2.EVENT_LBUTTONUP:
			self.mouseDrag = False
			self.activeFrame = None

		elif event == cv2.EVENT_MOUSEMOVE:
			if self.mouseDrag:
				if self.activeFrame != None:
					self.activeFrame.setSelected((x, y))
