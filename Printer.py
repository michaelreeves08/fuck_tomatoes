import serial
from settings import frameSettings
from utils import MatrixConversion

class Printer():
	def __init__(self, COM, bedSize):
		self.COM = COM
		self.max_X, self.max_Y = bedSize
		self.position = (0,0)
		self.packageExecuting = False
		self.settings = frameSettings.frameSettings()
		self.coeffs = MatrixConversion.find_coeffs(self.settings.image_frame.corners, self.settings.laser_frame.corners) 
		#try: self.ser = serial.Serial(self.COM, 115200, timeout = 1)
		#except: print("Connection Failure")

	def pointWithinBounds(self, xy):
		x, y = xy
		return (x > 0 and x < self.max_X) and (y > 0 and y < self.max_Y)

	def writePoint(self, xy):
		x,y = xy
		x = self.max_X - x
		self.position = xy
		command = 'G0 F5000 X%d Y%d\n'%(x, y) + 'G4 P1000\n' + 'G0 F5000 X0 Y0\n'

		if self.ser is not None and self.pointWithinBounds(xy):
			self.ser.write(command.encode())
			return 1
		else:
			return 0
	
	def writePackage(self, package):
		if self.ser is not None:
			self.packageExecuting = True
			self.ser.write(package.encode())

	def adjustXY(self, xy):
		printer_points = [(self.max_X,self.max_Y), (0,self.max_Y), (0,0), (self.max_X,0)]
		self.coeffs = MatrixConversion.find_coeffs(self.settings.laser_frame.corners, printer_points)
		return MatrixConversion.warped_xy((xy), self.coeffs)

	def write(self, xy):
		self.writePoint(self.adjustXY(xy))

	def buildGcodePackage(self, points):
		package = ''
		for point in points:
			if self.pointWithinBounds(point):
				x,y = point
				package += 'G0 F5000 X{:.3f} Y{:.3f}\n'.format(x, y)
				package += 'M106 S300\nG4 P500\nM107\n'
		package += 'G0 F5000 X0 Y0\n'
		return package

	def sendPackage(self, points):
		package = self.buildGcodePackage(list(map(self.adjustXY, points)))
		self.writePackage(package)

	def raiseZ(self):
		self.ser.write('G0 F5000 Z50\n'.encode())
	
	def callibrate(self):
		self.ser.write('G28\n'.encode())
	
	def home(self):
		self.ser.write('G0 F5000 X0 Y0\n'.encode())

	def read(self):
		print(self.ser.readline())