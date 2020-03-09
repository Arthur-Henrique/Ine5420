from app.model import Plane, Window, Vision, Perspective, Viewport, Clipping


class Landscape(Plane):
	distance = 10

	@property
	def window(self):
		return Window(self.center, self.angle, self.scale)

	@property
	def vision(self):
		return Vision(self.z)

	@property
	def perspective(self):
		return Perspective(self.center, self.distance)

	@property
	def viewport(self):
		return Viewport(
			self,
			tuple(20 for _ in self.origin),
			tuple(measure-40 for measure in self.area)
		)

	@property
	def clipping(self):
		return Clipping(
			tuple(20 for _ in self.origin),
			tuple(measure -40 for measure in self.area)
		)

	def __rmatmul__(self, draft):
		return draft \
				@ self.window \
				@ self.vision \
				@ self.perspective \
				@ self.viewport \
				@ self.clipping
