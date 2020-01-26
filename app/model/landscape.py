from app.model import Window, Viewport, Clipping

class Landscape:
	window = None
	viewport = None
	clipping = None

	def __init__(self, origin, area):
		x, y, width, height = (*origin, *area)

		self.window = Window(origin, area)
		self.viewport = Viewport((x+20, y+20), (width-40, height-40), self.window)
		self.clipping = Clipping((x+40, y+40), (width-80, height-80))

	def __rmatmul__(self, coordinates):
		return coordinates \
				@ self.window \
				@ self.viewport \
				@ self.clipping

	def draft(self):
		return [self.viewport, self.clipping]