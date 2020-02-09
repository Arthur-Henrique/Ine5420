from app.util import normalize, translate, perspective


class Perspective:
	distance = 0
	window = None

	def __init__(self, distance, window):
		self.distance = distance
		self.window = window

	def __rmatmul__(self, draft):
		draft.per_coordinate(self.transform)
		return draft

	def transform(self, coordinate):
		(cx, cy, cz) = self.perspective_center

		[x, y, z, w] = normalize(coordinate) \
						@ translate(-cx, -cy, -cz) \
						@ perspective(self.distance, coordinate[2]-cz) \
						@ translate(cx, cy, cz)

		return (x, y, z)

	@property
	def perspective_center(self):
		(x, y, z) = self.window.center
		return (x, y, z - self.distance)