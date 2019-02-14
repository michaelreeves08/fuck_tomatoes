import serial
from settings import frameSettings
from utils import MatrixConversion

class Printer():
	def __init__(self, COM):
		self.COM = COM
		self.max_X = 250
		self.max_Y = 200
		self.ser = None
		self.position = (0,0)
		self.sendSerial = False
		self.settings = frameSettings.frameSettings()
		self.coeffs = MatrixConversion.find_coeffs(self.settings.image_frame.corners, self.settings.laser_frame.corners) 

	def begin(self):
		print("Connecting")
		try:
			self.ser = serial.Serial(self.COM, 115200, timeout = 1)
		except:
			print("Connection Fail")

	def withinBounds(self, xy):
		x, y = xy
		return (x > 0 and x < self.max_X) and (y > 0 and y < self.max_Y)

	def writeRaw(self, xy):
		x,y = xy
		x = self.max_X - x
		self.position = xy
		command = 'G0 F5000 X%d Y%d\n'%(x, y) + 'G4 P1000\n' + 'G0 F5000 X0 Y0\n'

		if self.sendSerial and self.ser is not None and self.withinBounds(xy):
			self.ser.write(command.encode())
			return 1
		else:
			return 0
	
	def write(self, xy, laser_frame):
		galvo_points = [(self.max_X,self.max_Y), (0,self.max_Y), (0,0), (self.max_X,0)]
		self.coeffs = MatrixConversion.find_coeffs(laser_frame.corners, galvo_points)
		new_x, new_y = MatrixConversion.warped_xy( (xy), self.coeffs)
		self.writeRaw((new_x, new_y))

	def callibrate(self):
		self.ser.write('G28\n'.encode())
	
	def home(self):
		self.ser.write('G0 F5000 X0 Y0\n'.encode())

	def read(self):
		print(self.ser.readline())