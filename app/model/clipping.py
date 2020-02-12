from app.util import Frame
from core import __log__


class Clipping(Frame):

	def __rmatmul__(self, draft):
		draft.per_dot(lambda c: None if self.define_externality(*c) else c)
		draft.per_trace(self.transform)
		return draft

	def transform(self, line):
		externality = [self.define_externality(coordinate) for coordinate in line]

		if sum(externality[0]) & sum(externality[1]) != 0:
			return None
		elif sum(externality[0]) | sum(externality[1]) != 0:
			return self.clip(line.copy())
		else:
			return line

	# TODO 3D Clipping
	def clip(self, line):
		for i in [0, 1]:
			(x0, y0, z0) = line[i]
			(x1, y1, z1) = line[i-1]

			_x = x1 - x0
			_y = y1 - y0

			_c = (False, False)
			if x0 < self.left or x0 > self.right:
				limit = self.left if x0 < self.left else self.right
				m = _y / _x

				y0 = y0 + m * (limit - x0)
				x0 = limit

				if self.bottom < y0 < self.top:
					line = [(x0, y0, z0), line[i-1]]
					continue

			if y0 < self.bottom or y0 > self.top:
				limit = self.bottom if y0 < self.bottom else self.top
				m = _x / _y

				x0 = x0 + m * (limit - y0)
				y0 = limit

				if self.left < x0 < self.right:
					line = [(x0, y0, z0), line[i-1]]
				else:
					return None
		return line

	def define_externality(self, coordinate):
		(x, y, z) = coordinate

		externality = [
			side
			for (evaluation, side)
			in [
				(x < self.left, Externality.LEFT),
				(x > self.right, Externality.RIGTH),
				(y < self.bottom, Externality.BELLOW),
				(y > self.top, Externality.ABOVE)
			]
			if evaluation
		]

		return externality


class Externality:
	INSIDE = 0
	LEFT = 1
	RIGTH = 2
	BELLOW = 4
	ABOVE = 8
