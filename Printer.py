import serial, time
from settings import frameSettings
from utils import MatrixConversion, Geometry, Gcode, PrinterUtils

class Printer():
	def __init__(self, PrinterCOM, bedSize):
		self.COM = PrinterCOM
		self.max_X, self.max_Y = bedSize
		self.position = (0,0)
		self.sendSerial = False
		self.settings = frameSettings.frameSettings()
		self.coeffs = MatrixConversion.find_coeffs(self.settings.image_frame.corners, self.settings.laser_frame.corners) 
		try: self.printerSerial = serial.Serial(PrinterCOM, 115200, timeout = 25)
		except: print("Connection Failure")

	
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
		if self.printerSerial is not None:
			self.printerSerial.write(package.encode())

	def adjustXY(self, xy):
		printer_points = [(self.max_X,self.max_Y), (0,self.max_Y), (0,0), (self.max_X,0)]
		self.coeffs = MatrixConversion.find_coeffs(self.settings.laser_frame.corners, printer_points)
		return MatrixConversion.warped_xy((xy), self.coeffs)

	def write(self, xy):
		self.writePoint(self.adjustXY(xy))

	#Cannot send packages with over 4 locations at once,
	#it overflows the printer's serial buffer because it's a peice of dog shit
	def sendPackage(self, points):
		if points.count > 4: points = points[:4]
		package = Gcode.buildGcodePackage(list(map(self.adjustXY, points)), (self.max_X, self.max_Y))
		self.writePackage(package)

	def packageIsExecuting(self):
		#Query the printer for position
		#self.printerSerial.reset_input_buffer()
		self.printerSerial.write('M114'.encode())
		printerData = ''
		while self.printerSerial.in_waiting > 0:
			printerData += str(self.printerSerial.readline())
		if 'Count' in printerData:
			headPosition = PrinterUtils.parsePrinterXY(printerData)
			return not PrinterUtils.isHomed(headPosition)
		return True

	def raiseZ(self):
		self.printerSerial.write('G0 F5000 Z50\n'.encode())
	
	def callibrate(self):
		self.printerSerial.write('G28\n'.encode())
	
	def home(self):
		self.printerSerial.write('G0 F5000 X0 Y0\n'.encode())

	def read(self):
		print(self.printerSerial.readline())