from app.domain import Drawable

class Dot(Drawable):

	def __init__(self, **kwargs):
		assert len(kwargs['coordinates']) == 1, "Dot require exactly 1 coordinate"
		super().__init__(**kwargs)

class Trace(Drawable):

	def __init__(self, **kwargs):
		assert len(kwargs['coordinates']) == 2, "Trace require exactly 2 coordinates"
		super().__init__(**kwargs)


class Wireframe(Drawable):

	def __init__(self, **kwargs):
		assert len(kwargs['coordinates']) >= 3, "Wireframe require at least 3 coordinates"
		super().__init__(**kwargs)
