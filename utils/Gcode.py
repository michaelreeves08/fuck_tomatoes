from utils import Geometry

def buildGcodePackage(points, xyMax):
		package = 'G0 F5000\n'
		for point in points:
			if Geometry.pointWithinBounds(point, xyMax):
				x,y = point
				package += 'G0 X{:.1f} Y{:.1f}\n'.format(x, y)
				package += 'M106 S300\nG4 P500\nM107\n'
		package += 'G0 X0 Y0\n'
		return package