from app.model import Frame
from app.util import WORLD_CENTER, normalize, translate, scale, rotate


class Window(Frame):

	def __init__(self, center=WORLD_CENTER, angle=0, scale=1):
		self.center = center
		self.angle = angle
		self.scale = scale

	def __rmatmul__(self, draft):
		draft.per_coordinate(self.transform)
		return draft

	def transform(self, coordinate, **kwargs):
		(cx, cy, cz) = self.center

		[x, y, z, _] = normalize(coordinate) \
					@ translate(-cx, -cy, 0) \
					@ scale(self.scale) \
					@ rotate(-self.angle) \
					@ translate(cx, cy, 0)

		return (x, y, z)