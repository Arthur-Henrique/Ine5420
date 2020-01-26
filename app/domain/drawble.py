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


class Drawable(Object):
	color = (1, 1, 1)

	def __init__(self, **kwargs):
		self.coordinates = kwargs['coordinates']
		assert all(len(coordinate) == self.dimension for coordinate in self.coordinates),\
			"Coordinates with same dimention type is required"
		super().__init__(**kwargs)

	@property
	def origin(self):
		return self.coordinates[0]

	@property
	def center(self):
		return (
			sum(x for x, _, _ in self.coordinates) / self.grade,
			sum(y for _, y, _ in self.coordinates) / self.grade,
			sum(z for _, _, z in self.coordinates) / self.grade
		)

	@property
	def origin(self):
		return self.coordinates[0]

	@property
	def dimension(self):
		return len(self.origin)

	@property
	def grade(self):
		return len(self.coordinates)

	@property
	def draft(self):
		return self.coordinates

	def __str__(self):
		return super().__str__() + f"\n\t{self.draft}"

