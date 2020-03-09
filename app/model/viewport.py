from app.model import Frame


class Viewport(Frame):

	def __init__(self, landscape, origin, area):
		self.landscape = landscape
		self.origin = origin
		self.area = area

	def __rmatmul__(self, draft):
		draft.per_coordinate(self.transform)
		return draft

	def transform(self, coordinate, **kwargs):
		x, y, z = coordinate

		vx, vy, vz = self.origin
		width, height = self.area

		x = vx + (x - self.landscape.x) * width / self.landscape.width
		y = vy + (y - self.landscape.y) * height / self.landscape.height

		return (x, y, z)
