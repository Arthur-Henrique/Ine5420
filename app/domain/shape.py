from app.domain import Drawable
from app.util import matrix


class Point(Drawable):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.require_grade('exactly', 1)

	@property
	def draft(self):
		return {'Dot': [self.coordinates]}


class Line(Drawable):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.require_grade('exactly', 2)

	@property
	def draft(self):
		return {'Trace': [self.coordinates]}


class Chain(Drawable):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.require_grade('at least', 3)

	@property
	def draft(self):
		return {'Trace': [self.coordinates[i:i+2] for i in range(self.grade-1)]}


class Polygon(Chain):

	@property
	def draft(self):
		draft = super(Polygon, self).draft
		draft['Trace'].append([self.coordinates[-1], self.origin])
		return draft


class Curve(Drawable):
	delta = 0.01

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.require_grade('at least', 4)


# TODO: Allow more than 4 coordinates
class BezierCurve(Curve):

	@property
	def draft(self):
		gx, gy, gz = matrix.geometry(self.coordinates)

		t = 0
		bezier = []
		while t < 1:
			x, y, z = ((matrix.bezier(t) @ g)[0] for g in (gx, gy, gz))
			bezier.append((x, y, z))

			t += self.delta

		return {'Trace': [bezier[i:i+2] for i in range(len(bezier)-1)]}


class BSpineCurve(Curve):
	@property
	def draft(self):
		i = 4
		bspine = []
		while i <= len(self.coordinates):
			gx, gy, gz = matrix.geometry(self.coordinates[i - 4:i])

			cx, cy = (matrix.bspine() @ g for g in (gx, gy))

			dx = [d[0] for d in matrix.initial_differences(self.delta) @ cx]
			dy = [d[0] for d in matrix.initial_differences(self.delta) @ cy]

			j = 0
			forward_differences = lambda d: [sum(d[i - 2:i]) for i in range(2, len(d)+1)]
			while j < 1.0:
				bspine.append((dx[0], dy[0], 0))
				(dx, dy) = (forward_differences(d + [0]) for d in (dx, dy))

				j += self.delta
			i += 1

		return {'Trace': [bspine[i-2:i] for i in range(2, len(bspine))]}
