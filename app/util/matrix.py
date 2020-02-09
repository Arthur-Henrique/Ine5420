from numpy import array, cos, sin

def matriz(m):
	return array(m, dtype=float)


# Transformation

def normalize(coordinate):
	(x, y, z) = coordinate
	return matriz([x, y, z, 1])


def translate(x, y, z):
	return matriz((
		[1, 0, 0, 0],
		[0, 1, 0, 0],
		[0, 0, 1, 0],
		[x, y, z, 1]
	))


def rotate(angle, axis='z'):
	c = cos(angle)
	s = sin(angle)

	option = {
		'x': matriz((
			[1, 0, 0, 0],
			[0, c, -s, 0],
			[0, s, c, 0],
			[0, 0, 0, 1]
		)),
		'y': matriz((
			[c, 0, -s, 0],
			[0, 1, 0, 0],
			[s, 0, c, 0],
			[0, 0, 0, 1]
		)),
		'z': matriz((
			[c, -s, 0, 0],
			[s, c, 0, 0],
			[0, 0, 1, 0],
			[0, 0, 0, 1]
		))
	}

	return option[axis]


def scale(s):
	return matriz((
		[s, 0, 0, 0],
		[0, s, 0, 0],
		[0, 0, 1, 0],
		[0, 0, 0, 1]

	))


def geometry(coordinates):
	return [
		matriz([
			[coordinate[i]]
			for coordinate
			in coordinates
		])
		for i in range(len(coordinates[0]))
	]


# Curve

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
	return matriz([t ** 3, t ** 2, t, 1]) \
			@ matriz((
				[-1, 3, -3, 1],
				[3, -6, 3, 0],
				[-3, 3, 0, 0],
				[1, 0, 0, 0]
			))

# Perspective


def perspective(d, z):
	return matriz((
		[d/z, 0, 0, 0],
		[0, d/z, 0, 0],
		[0, 0, d/z, 0],
		[0, 0, 0,   1]
	))


def direction(line, z):
	[begin, end] = line

	vector = [
		end[i] - begin[i]
		for i in range(3)
	]
	magnitude = sum(axis ** 2 for axis in vector) ** (1 / 2)
	_z = begin[2] - z

	return translate(*(_z * axis / magnitude for axis in vector))
