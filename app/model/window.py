from app.util import math, Frame, normalize, translate, scale, rotate
from core import __project__


class Window(Frame):
	angle = None
	scale = None

	def __init__(self, origin, area, angle=0, scale=1):
		super().__init__(origin, area)

		self.angle = math.radians(angle)
		self.scale = scale

	def move(self, measure, direction):
		[dx, dy, dz, _] = normalize(direction) @ rotate(self.angle)

		self.origin = (
			self.x + measure * dx,
			self.y + measure * dy,
			self.z + measure * dz
		)

		__project__("window_transformation")

	def turn(self, measure, direction):
		self.angle += math.radians(measure * direction[0])
		self.angle %= math.radians(360)

		__project__("window_transformation")

	def __rmatmul__(self, draft):
		draft.per_coordinate(self.transform)
		return draft

	def transform(self, coordinate):
		(cx, cy, cz) = self.center

		[x, y, z, _] = normalize(coordinate) \
					@ translate(-cx, -cy, 0) \
					@ scale(self.scale) \
					@ rotate(-self.angle) \
					@ translate(cx, cy, 0)

		return (x, y, z)
