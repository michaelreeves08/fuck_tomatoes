import numpy as np

def find_coeffs(pa, pb):
	matrix = []
	for p1, p2 in zip(pa, pb):
		matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
		matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])
	
	A = np.matrix(matrix, dtype=np.float)
	B = np.array(pb).reshape(8)
	
	res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
	return np.array(res).reshape(8)

def warped_xy(xy, coeffs):
	x_in = xy[0]
	y_in = xy[1]
	
	#x = (ax+by+c)/(gx+hy+1)
	#y = (dx+ey+f)/(gy+hy+1)
	warped_x = (coeffs[0]*x_in + coeffs[1]*y_in + coeffs[2]) / (coeffs[6]*x_in + coeffs[7]*y_in + 1)
	warped_y = (coeffs[3]*x_in + coeffs[4]*y_in + coeffs[5]) / (coeffs[6]*x_in + coeffs[7]*y_in + 1)
	return (warped_x, warped_y)