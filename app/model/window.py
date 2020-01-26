from app.util import math, Rectangle, normalize, translate, scale, rotate
from core import __project__


class Window(Rectangle):
	angle = None
	scale = None

	def __init__(self, origin, area, angle=0, scale=1):
		super().__init__(origin, area)

		self.angle = math.radians(angle)
		self.scale = scale

	def move(self, measure, direction):
		[[dx, dy, *_]] = normalize([direction]) @ rotate(self.angle)

		self.origin = (
			self.x + measure * dx,
			self.y + measure * dy
		)

		__project__("window_transformation")

	def turn(self, measure, direction):
		self.angle += math.radians(measure * direction[0])
		self.angle %= math.radians(360)

		__project__("window_transformation")

	def zoom(self, measure, direction):
		self.scale *= 1 + measure / 100 * direction[1]
		__project__("window_transformation")

	def __rmatmul__(self, coordinates):
		(cx, cy, cz) = self.center

		representation = []
		for coordinate in normalize(coordinates):
			[x, y, z, _] = coordinate \
						@ translate(-cx, -cy) \
						@ scale(self.scale) \
						@ rotate(-self.angle) \
						@ translate(cx, cy)

			representation.append((x, y))
		return representation
