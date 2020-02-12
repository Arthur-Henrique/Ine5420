from app.domain import Drawable
from app.util import matrix, calculate_bspine, transpose


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

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.require_grade('at least', 4)


# TODO: Allow more than 4 coordinates
class BezierCurve(Curve):
	delta = 0.01

	@property
	def draft(self):
		_g = matrix.geometry(self.coordinates)

		_c = [matrix.bezier() @ g for g in _g]

		t = 0
		bezier = []
		while t < 1:
			x, y, z = ((matrix.pow(t, 3) @ c)[0] for c in _c)
			bezier.append((x, y, z))

			t += self.delta

		return {'Trace': [bezier[i:i+2] for i in range(len(bezier)-1)]}


class BSpineCurve(Curve):

	@property
	def draft(self):
		bspine = calculate_bspine(self.coordinates)
		return {'Trace': [bspine[i - 2:i] for i in range(2, len(bspine))]}


class Surface(Drawable):
	delta = 0.1

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.require_grade('at least', 16)

	@property
	def geometry(self):
		_g = [[c[i] for c in self.coordinates] for i in range(3)]
		return [[g[i - 4:i] for i in range(4, 17, 4)] for g in _g]


class BezierSurface(Surface):

	@property
	def draft(self):
		_g = self.geometry

		_c = [
			matrix.bezier() \
			@ g \
			@ matrix.bezier() \
			for g in _g
		]

		trace = []
		s = 0
		while s < 1:

			t = 0
			bezier = []
			while t < 1:
				(x, y, z) = [
					matrix.pow(s, 3) \
					@ c \
					@ matrix.pow(t, 3, transpose=True) \
					for c in _c
				]
				bezier.append((x, y, z))
				t += self.delta

			trace.extend([bezier[i - 2:i] for i in range(2, len(bezier))])

			s += self.delta

		return {'Trace': trace}


class BSpineSurface(Surface):

	@property
	def draft(self):
		_g = self.geometry

		_c = [
			matrix.bspine() \
			@ g \
			@ matrix.bspine(transpose=True) \
			for g in _g
		]

		_d = lambda: [
			[
				matrix.init_diff(self.delta) \
				@ c \
				@ matrix.init_diff(self.delta, transpose=True)
			]
			[0].tolist()
			for c in _c
		]

		return {'Trace': self.dash(_d()) + self.dash([transpose(d) for d in _d()])}

	def dash(self, _d):
		first_row = lambda _f: \
			list(
				tuple(
					f[0][j]
					for f in _f
				)
				for j in range(4)
			)

		s = 0
		trace = []
		while s < 1:
			bspine = calculate_bspine(first_row(_d))
			trace.extend([bspine[i - 2:i] for i in range(2, len(bspine))])

			_d = [
				matrix.forward_diff() @ d
				for d in _d
			]

			s += self.delta

		return trace




