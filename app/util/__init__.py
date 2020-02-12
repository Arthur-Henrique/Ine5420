WORLD_CENTER = (0, 0, 0)

from app.util.matrix import *
from app.util.frame import *
import math

class Direction:
	UP = (0, -1, 0)
	LEFT = (-1, 0, 0)
	DOWN = (0, 1, 0)
	RIGHT = (1, 0, 0)
	FORWARD = (0, 0, 1)
	BACKWARD = (0, 0, -1)

def calculate_bspine(reference, delta=0.01):
	i = 4
	coordinates = []
	while i <= len(reference):
		_g = matrix.geometry(reference[i-4:i])

		_c = [
			matrix.bspine() @ g
			for g in _g
		]

		_d = [
			matrix.init_diff(delta) @ c
			for c in _c
		]

		j = 0
		while j < 1.0:
			x, y, z = (d[0, 0] for d in _d)
			coordinates.append((x, y, z))

			_d = [
				forward_diff() @ d
				for d in _d
			]

			j += delta
		i += 1

	return coordinates
