from numpy import array, cos, sin

def matriz(m):
	return array(m, dtype=float)


# Transformation

def base():
	return matriz((
		[1, 0, 0],
		[0, 1, 0],
		[0, 0, 1]
	))


def normalize(coordinates):
	return [matriz([x, y, 1]) for (x, y) in coordinates]


def translate(x, y):
	return matriz((
		[1, 0, 0],
		[0, 1, 0],
		[x, y, 1]
	))


def rotate(angle):
	c = cos(angle)
	s = sin(angle)

	return matriz((
		[c, -s, 0],
		[s, c, 0],
		[0, 0, 1]
	))

def scale(scale):
	return matriz((
		[scale, 0, 0],
		[0, scale, 0],
		[0, 0, 1]
	))


# Curve

def geometry(coordinates):
	result = []

	i = 0
	while i < len(coordinates[0]):
		m = matriz([[coordinate[i]] for coordinate in coordinates])
		result.append(m)

		i += 1

	return result

def bspine():
	return matriz((
		[-1, 3, -3, 1],
		[3, -6, 3, 0],
		[-3, 0, 3, 0],
		[1, 4, 1, 0]
	)) / 6


def initial_differences(d):
	d, d2, d3 = (d ** i for i in range(1, 4))

	return matriz((
		[0, 0, 0, 1],
		[d3, d2, d, 0],
		[6 * d3, 2 * d2, 0, 0],
		[6 * d3, 0, 0, 0]
	))

def bezier(t):
	return matriz([t ** 3, t ** 2, t, 1]) @ matriz((
		[-1, 3, -3, 1],
		[3, -6, 3, 0],
		[-3, 3, 0, 0],
		[1, 0, 0, 0]
	))
