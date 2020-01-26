from numpy import array, cos, sin

def matriz(m):
	return array(m, dtype=float)


# Transformation

def normalize(coordinates):
	return [matriz([x, y, z, 1]) for (x, y, z) in coordinates]


def translate(x, y, z):
	return matriz((
		[1, 0, 0, 0],
		[0, 1, 0, 0],
		[0, 0, 1, 0]
		[x, y, z, 1]
	))


def rotate_x(angle):
	c = cos(angle)
	s = sin(angle)

	return matriz((
		[1, 0, 0, 0],
		[0, c, -s, 0],
		[0, s, c, 0],
		[0, 0, 0, 1]
	))

def rotate_y(angle):
	c = cos(angle)
	s = sin(angle)

	return matriz((
		[c, 0, -s, 0],
		[0, 1, 0, 0],
		[s, 0, c, 0],
		[0, 0, 0, 1]
	))

def rotate_z(angle):
	c = cos(angle)
	s = sin(angle)

	return matriz((
		[c, -s, 0, 0],
		[s, c, 0, 0],
		[0, 0, 1, 0],
		[0, 0, 0, 1]
	))

def scale(s):
	return matriz((
		[s, 0, 0, 0],
		[0, s, 0, 0],
		[0, 0, s, 0],
		[0, 0, 0, 1]
	))