from utils import Geometry

def buildGcodePackage(points, xyMax, withSpike):
		package = 'G0 F5000\n' #Set printer head speed
		for point in points:
			if Geometry.pointWithinBounds(point, xyMax):
				x,y = point
				package += 'G0 X{:.1f} Y{:.1f}\n'.format(x, y) #Positioning format
				#Pnumatic trigger on/off
				if withSpike: package += 'M106 S300\n'
				package += 'G4 P500\n'
				if withSpike: package += 'M107\n'
		package += 'G0 X0 Y0\n'
		return package