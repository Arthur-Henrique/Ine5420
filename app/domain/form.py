from app.domain import Geometric
from app.util import matrix, calculate_bspine, transpose


class Form(Geometric):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		assert kwargs['name'], 'Name is required'
		self.__dict__.update(kwargs)

	@property
	def type(self):
		return self.__class__.__name__

	def __str__(self):
		return f"\n\t{self.id}:\t{self.type}, {self.name}\n" + super().__str__()


class Point(Form):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.require_grade('exactly', 1)

	@property
	def draft(self):
		return {'Dot': [self.scribble(self.coordinates)]}


class Line(Form):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.require_grade('exactly', 2)

	@property
	def draft(self):
		return {'Trace': [self.scribble(self.coordinates)]}


class Chain(Form):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.require_grade('at least', 3)

	@property
	def draft(self):
		return {'Trace':  [
					self.scribble(self.coordinates[i:i+2])
					for i in range(self.grade-1)
				]}


class Polygon(Chain):

	@property
	def draft(self):
		traces = [
			self.coordinates[i:i + 2]
			for i in
			range(self.grade-1)
		] + [[self.coordinates[-1], self.origin]]

		return {'Trace': [
			self.scribble(trace)
			for trace in traces
		]}


class Face(Polygon):

	@property
	def draft(self):
		return {'Face': [self.scribble(self.coordinates)]}


class Curve(Form):

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

		return {'Trace': [
					self.scribble(bezier[i:i+2])
					for i in range(len(bezier)-1)
				]}


class BSpineCurve(Curve):

	@property
	def draft(self):
		bspine = calculate_bspine(self.coordinates)
		return {'Trace': [
					self.scribble(bspine[i:i+2])
					for i in range(len(bspine)-1)
				]}


class Surface(Form):
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

		dashed = []
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

			dashed.extend([bezier[i:i+2] for i in range(len(bezier)-1)])

			s += self.delta

		return {'Trace': [
					self.scribble(trace)
					for trace in dashed
				]}


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

		dashed = self.dashed(_d()) + self.dashed([transpose(d) for d in _d()])

		return {'Trace': [
					self.scribble(trace)
					for trace in dashed
				]}

	def dashed(self, _d):
		first_row = lambda _f: \
			list(
				tuple(
					f[0][j]
					for f in _f
				)
				for j in range(4)
			)

		k = 0
		dashed = []
		while k < 1:
			bspine = calculate_bspine(first_row(_d))
			dashed.extend([bspine[i:i+2] for i in range(len(bspine)-1)])

			_d = [
				matrix.forward_diff() @ d
				for d in _d
			]

			k += self.delta

		return dashed
