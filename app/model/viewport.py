from app.util import Frame


class Viewport(Frame):
	window = None

	def __init__(self, origin, area, window):
		super().__init__(origin, area)
		self.window = window

	def __rmatmul__(self, draft):
		draft.per_coordinate(self.transform)
		return draft

	def transform(self, coordinate):
		(x, y, z) = coordinate

		x = self.x + (x - self.window.x) * self.width / self.window.width
		y = self.y + (y - self.window.y) * self.height / self.window.height

		return (x, y, z)
