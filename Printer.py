import serial
from settings import frameSettings
from utils import MatrixConversion, Geometry, Gcode

class Printer():
	def __init__(self, PrinterCOM, SensorCOM, bedSize):
		self.COM = PrinterCOM
		self.max_X, self.max_Y = bedSize
		self.position = (0,0)
		self.settings = frameSettings.frameSettings()
		self.coeffs = MatrixConversion.find_coeffs(self.settings.image_frame.corners, self.settings.laser_frame.corners) 
		# try: 
		# 	self.printerSerial = serial.Serial(PrinterCOM, 115200, timeout = 1)
		# 	self.sensorSerial = serial.Serial(SensorCOM, 9600, timeout = 25)
		# except:
		# 	print("Connection Failure")

	
	def writePoint(self, xy):
		x,y = xy
		x = self.max_X - x
		self.position = xy
		command = 'G0 F5000 X%d Y%d\n'%(x, y) + 'G4 P1000\n' + 'G0 F5000 X0 Y0\n'

		if self.printerSerial is not None and Geometry.pointWithinBounds(xy, (self.max_X, self.max_Y)):
			self.printerSerial.write(command.encode())
			return 1
		else:
			return 0
	
	def writePackage(self, package):
		#Send signal to execution sensor

		if self.printerSerial is not None:
			self.sensorSerial.write('1'.encode())
			self.printerSerial.write(package.encode())

	def adjustXY(self, xy):
		printer_points = [(self.max_X,self.max_Y), (0,self.max_Y), (0,0), (self.max_X,0)]
		self.coeffs = MatrixConversion.find_coeffs(self.settings.laser_frame.corners, printer_points)
		return MatrixConversion.warped_xy((xy), self.coeffs)

	def write(self, xy):
		self.writePoint(self.adjustXY(xy))

	def sendPackage(self, points):
		package = Gcode.buildGcodePackage(list(map(self.adjustXY, points)))
		self.writePackage(package)

	def packageIsExecuting(self):
		if self.sensorSerial.in_waiting > 0:
			status = self.sensorSerial.read()
			if status is not None:
				self.sensorSerial.write('0'.encode())
				#Might have to add delay here depending on how quick that shit writes
				self.sensorSerial.reset_input_buffer()
				return False
		return True

	def raiseZ(self):
		self.printerSerial.write('G0 F5000 Z50\n'.encode())
	
	def callibrate(self):
		self.printerSerial.write('G28\n'.encode())
	
	def home(self):
		self.printerSerial.write('G0 F5000 X0 Y0\n'.encode())

	def read(self):
		print(self.printerSerial.readline())