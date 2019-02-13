import serial
from utils import MatrixConversion

class Printer():
	def __init__(self, COM, coeffs):
		self.COM = COM
		self.coeffs = coeffs 
		self.max_X = 250
		self.max_Y = 200
		self.ser = None
		self.position = (0,0)

	def begin(self):
		print("Connecting")
		try:
			pass
			#self.ser = serial.Serial('COM5', 9600, timeout=1)
			#time.sleep(3)
		except:
			print("Connection Fail")

	def withinBounds(self, xy):
		x, y = xy
		return (x > 0 and x < self.max_X) and (y > 0 and y < self.max_Y)

	def writeRaw(self, xy):
		x,y = xy
		self.position = xy
		command = 'G0 F5000 X%d Y%d'%(x, y)

		if self.withinBounds(xy):
			print(command)
		else:
			print('out of bounds')
		# if self.ser not None:
		# 	#self.ser.write(command.encode())
		# 	return 1
		# else:
		# 	return 0
	
	def write(self, xy, laser_frame):
		galvo_points = [(self.max_X,self.max_Y), (0,self.max_Y), (0,0), (self.max_X,0)]
		self.coeffs = MatrixConversion.find_coeffs(laser_frame.corners, galvo_points)
		new_x, new_y = MatrixConversion.warped_xy( (xy), self.coeffs)
		self.writeRaw((new_x, new_y))

	def read(self):
		print(ser.readline())