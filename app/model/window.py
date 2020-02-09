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
		[dx, dy, *_] = normalize(direction) @ rotate(self.angle)

		self.origin = (
			self.x + measure * dx,
			self.y + measure * dy,
			self.z
		)

		__project__("window_transformation")

	def turn(self, measure, direction):
		self.angle += math.radians(measure * direction[0])
		self.angle %= math.radians(360)

		__project__("window_transformation")

	def zoom(self, measure, direction):
		# self.scale *= 1 + measure / 100 * direction[1]
		self.origin = (
			self.x,
			self.y,
			self.z + measure * direction[1]
		)
		__project__("window_transformation")

	def __rmatmul__(self, draft):
		draft.per_coordinate(self.transform)
		return draft

	def transform(self, coordinate):
		(cx, cy, cz) = self.center
		(ox, oy, oz) = self.origin

		[x, y, z, _] = normalize(coordinate) \
					@ translate(-cx, -cy, 0) \
					@ scale(self.scale) \
					@ rotate(-self.angle) \
					@ translate(cx, cy, 0)
					# @ translate(-ox, -oy, -oz)

		return (x, y, z)
