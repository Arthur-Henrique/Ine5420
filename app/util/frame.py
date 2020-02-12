from abc import abstractmethod
from app.util import WORLD_CENTER

class Rectangle:
	origin = None
	area = None

	def __init__(self, origin=WORLD_CENTER, area=(100, 100)):
		self.origin = origin
		self.area = area

	@property
	def x(self):
		return self.origin[0]

	@property
	def y(self):
		return self.origin[1]

	@property
	def z(self):
		return self.origin[2]

	@property
	def width(self):
		return self.area[0]

	@property
	def height(self):
		return self.area[1]

	@property
	def center(self):
		return (
			self.x + self.width / 2,
			self.y + self.height / 2,
			self.z
		)

	@property
	def end(self):
		return (
			self.x + self.width,
			self.y + self.height,
			self.z
		)

	@property
	def left(self):
		return self.x

	@property
	def right(self):
		return self.x + self.width

	@property
	def bottom(self):
		return self.y

	@property
	def top(self):
		return self.y + self.height

	@property
	def description(self):
		return (*self.origin, *self.area)

	@property
	def vertices(self):
		return [
			self.origin,
			(self.x + self.width, self.y, self.z),
			self.end,
			(self.x, self.y + self.height, self.z)
		]

	@property
	def draft(self):
		vertices = self.vertices + [self.origin]

		return {
			'Dot': [[self.center]],
			'Trace': [vertices[i:i+2] for i in range(len(vertices) - 1)]
		}


class Frame(Rectangle):
	@abstractmethod
	def __rmatmul__(self, draft):
		pass

	@abstractmethod
	def transform(self, scribble):
		pass
