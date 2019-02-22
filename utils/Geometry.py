def distance(point_a, point_b):
	return (((point_b[0] - point_a[0]) ** 2 + (point_b[1] - point_a[1]) ** 2) ** (0.5))

def pointWithinBounds(xy, xyMax):
		x, y = xy
		max_X, max_Y = xyMax
		return (x > 0 and x < max_X) and (y > 0 and y < max_Y)