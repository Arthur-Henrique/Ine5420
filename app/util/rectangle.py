from app.util import WORLD_CENTER
from app.domain import Drawable


class Rectangle(Drawable):
	origin = None
	area = None

	def __init__(self, origin=WORLD_CENTER, area=(100, 100)):
		super().__init__()
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
	def center(self):
		return (
			self.x + self.width/2,
			self.y + self.height/2,
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
	def coordinates(self):
		return [
			self.origin,
			(self.x + self.width, self.y, self.z),
			self.end,
			(self.x, self.y + self.height, self.z)
		]

	@property
	def width(self):
		return self.area[0]

	@property
	def height(self):
		return self.area[1]

	@property
	def draft(self):
		vertices = self.coordinates + [self.origin]

		return {
			'Dot': [self.scribble([self.center])],
			'Trace': [
				self.scribble(vertices[i:i+2])
				for i in range(len(vertices)-1)
			]
		}

	def __str__(self):
		return f'{self.origin}, {self.area} '
