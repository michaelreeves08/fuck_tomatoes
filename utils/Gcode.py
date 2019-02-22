from utils import Geometry

def buildGcodePackage(points):
		package = ''
		for point in points:
			if Geometry.pointWithinBounds(point):
				x,y = point
				package += 'G0 F5000 X{:.3f} Y{:.3f}\n'.format(x, y)
				package += 'M106 S300\nG4 P500\nM107\n'
		package += 'G0 F5000 X0 Y0\n'
		return package