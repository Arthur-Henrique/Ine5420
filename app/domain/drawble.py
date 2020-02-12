from abc import abstractmethod

from core import __require__


class Object:

	def __init__(self, **kwargs):
		assert kwargs['name'], 'Name is required'
		self.__dict__.update(kwargs)

	@property
	def type(self):
		return self.__class__.__name__

	def __str__(self):
		pass
		return f"\n\t{self.id}:\t{self.type}, {self.name}"

	def __getitem__(self, key):
		return self.__dict__[key]


class Drawable(Object):
	color = None
	coordinates = []

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		assert kwargs['color'], 'Color is required'
		self.require_dimension()

		if not self.color:
			self.color = (0, 0, 0)

	@property
	def origin(self):
		return self.coordinates[0]

	@property
	def center(self):
		return (
			sum(coordinate[i] for coordinate in self.coordinates)
			for i in range(self.dimension)
		)

	@property
	def dimension(self):
		return len(self.origin)

	@property
	def grade(self):
		return len(self.coordinates)

	@property
	@abstractmethod
	def draft(self):
		pass

	def __str__(self):
		return super().__str__() + f"\n\t{self.draft}"

	def require_grade(self, relation, grade):
		__require__(
			{
				'exactly': lambda g: g == grade,
				'at least': lambda g: g >= grade
			}[relation],
			f"{self.type} require {relation} {grade} coordinates",
			self.grade
		)

	def require_dimension(self):
		__require__(
			lambda c: len(c) == self.dimension,
			"All coordinates are required to have same dimension",
			*self.coordinates,
		)
