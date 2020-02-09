from app.model import Window, Vision, Perspective, Viewport, Clipping


class Landscape:
	window = None
	vision = None
	perspective = None
	viewport = None
	clipping = None

	def __init__(self, origin=(0, 0, 0), area=(100, 100), distance=10):
		x, y, z, width, height = (*origin, *area)

		self.window = Window(origin, area)
		self.vision = Vision(self.window)
		self.perspective = Perspective(distance, self.window)
		self.viewport = Viewport((x+20, y+20, z), (width-40, height-40), self.window)
		self.clipping = Clipping((x+20, y+20, z), (width-40, height-40))

	def __rmatmul__(self, draft):
		draft = draft \
				@ self.window \
				@ self.vision \
				@ self.perspective \
				@ self.viewport \
				@ self.clipping

		draft + self.clipping.draft

		return draft
