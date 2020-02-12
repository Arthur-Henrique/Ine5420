from numpy import array, cos, sin, transpose


def matriz(m):
	return array(m, dtype=float)


def transposable(m_func):
	def decorated(*args, **kwargs):
		m = m_func(*args)

		return m if not 'transpose' in kwargs.keys() else transpose(m)

	return decorated

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
		matriz((
			[
				[coordinate[i]]
				for coordinate
				in coordinates
			]
		))
		for i in range(3)
	]


# Curve

@transposable
def bspine():
	return matriz((
		[-1, 3, -3, 1],
		[3, -6, 3, 0],
		[-3, 0, 3, 0],
		[1, 4, 1, 0]
	)) / 6


@transposable
def init_diff(d):
	[d3, d2, d, _] = pow(d, 3)

	m = matriz((
		[0, 0, 0, 1],
		[d3, d2, d, 0],
		[6 * d3, 2 * d2, 0, 0],
		[6 * d3, 0, 0, 0]
	))

	return m


def bezier():
	return matriz((
			[-1, 3, -3, 1],
			[3, -6, 3, 0],
			[-3, 3, 0, 0],
			[1, 0, 0, 0]
		))


@transposable
def forward_diff():
	return matriz((
		[1, 1, 0, 0],
		[0, 1, 1, 0],
		[0, 0, 1, 1],
		[0, 0, 0, 1],
	))


@transposable
def pow(b, i):
	return matriz([b ** p for p in range(i, -1, -1)])


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
