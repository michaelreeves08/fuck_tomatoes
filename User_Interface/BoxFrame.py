from utils import MatrixConversion, Geometry

class BoxFrame():
	def __init__(self, corners):
		self.corners = corners
		self.selectedCorner = None

	def isTouching(self, cursorPos, diameter):
		index = 0
		for point in self.corners:
			if Geometry.distance(cursorPos, point) <= diameter:
				self.selectedCorner = index
				return True
			else:
				index += 1
		# no touching corner
		return False

	def setSelected(self, point):
		self.corners[self.selectedCorner] = point

	# geometric center
	def getCentroid(self):
		x_total, y_total = 0, 0
		for x, y in self.corners:
			x_total += x
			y_total += y
		return ((x_total / 4), (y_total / 4))

	def getCenter(self):
		xy = (0,0)
		simple = [(0,0),(1,0),(1,1),(0,1)]
		coeffs = MatrixConversion.find_coeffs(simple, self.corners)
		return MatrixConversion.warped_xy((0.5, 0.5), coeffs)

	def getSize(self):
		x_min, x_max, y_min, y_max = 0, 0, 0, 0
		for x, y in self.corners:
			x_min = x if x < x_min else x_min
			x_max = x if x > x_max else x_max
			y_min = y if y < y_min else y_min
			y_max = y if y > y_max else y_max
		return (x_max - x_min, y_max - y_min)