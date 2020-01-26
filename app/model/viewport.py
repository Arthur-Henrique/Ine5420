from app.util import Rectangle


class Viewport(Rectangle):
	window = None

	def __init__(self, origin, area, window):
		super().__init__(origin, area)
		self.window = window

	def __rmatmul__(self, coordinates):
		representation = []
		for (x, y) in coordinates:
			x = self.x + (x - self.window.x) * self.width / self.window.width
			y = self.y + (y - self.window.y) * self.height / self.window.height

			representation.append((x, y))
		return representation
