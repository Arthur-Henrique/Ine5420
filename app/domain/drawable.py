from abc import abstractmethod
from core import __require__


class Drawable:

	def __init__(self, color=(.5, .5, .5), **kwargs):
		self.color = color

	@property
	@abstractmethod
	def draft(self):
		pass

	def scribble(self, coordinates):
		return dict(
			coordinates=coordinates,
			color=self.color
		)

	def __str__(self):
		return super().__str__() + f"\n\t{self.draft}"


class Geometric(Drawable):

	def __init__(self, coordinates, **kwargs):
		super().__init__(**kwargs)
		self.coordinates = coordinates

	@property
	def origin(self):
		return self.coordinates[0]

	@property
	def center(self):
		return tuple(
			sum(
				coordinate[i] / self.grade
				for coordinate
				in self.coordinates
			)
			for i in range(self.dimension)
		)

	@property
	def dimension(self):
		return len(self.origin)

	@property
	def grade(self):
		return len(self.coordinates)

	def __str__(self):
		return f"\t{self.coordinates}"

	def require_grade(self, relation, grade):
		__require__(
			{
				'exactly': lambda g: g == grade,
				'at least': lambda g: g >= grade
			}[relation],
			f"{self.type} require {relation} {grade} coordinates",
			self.grade
		)