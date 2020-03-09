from app.model import Frame
from app.util import normalize, translate, perspective


class Perspective(Frame):

	def __init__(self, center, distance):
		self.center = center
		self.distance = distance

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
		(x, y, z) = self.center
		return (x, y, z - self.distance)