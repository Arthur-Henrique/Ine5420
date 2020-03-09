from app.util import WORLD_CENTER, Rectangle, normalize, rotate, math
from core import __log__, __project__


class Plane(Rectangle):

	def __init__(self, origin=WORLD_CENTER, area=(750, 750), angle=0, scale=1):
		super(Plane, self).__init__(origin, area)
		self.angle = angle
		self.scale = scale

	def move(self, measure, direction):
		[dx, dy, dz, _] = normalize(direction) @ rotate(self.angle)

		self.origin = (
			self.x + measure * dx,
			self.y + measure * dy,
			self.z + measure * dz
		)

		__log__(landscape=str(self))
		__project__("landscape")

	def turn(self, measure, direction):
		self.angle += math.radians(measure * direction[0])
		self.angle %= math.radians(360)

		__log__(landscape=str(self))
		__project__("landscape")

	def zoom(self, measure, direction):
		self.scale *= 1 + measure / 100 * direction[2]

		__log__(landscape=str(self))
		__project__("landscape")

	def recenter(self, center):
		direction = tuple(end - begin for begin, end in zip(self.center, center))
		self.move(1, direction)

	def resize(self, area):
		self.area = area

	def __str__(self):
		return super().__str__() + f' {self.angle}º {self.scale}+'
