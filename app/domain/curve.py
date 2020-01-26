from app.domain import Drawable
from app.util import matrix
from abc import abstractmethod


class Curve(Drawable):
	delta = 0.01

	def __init__(self, **kwargs):
		assert len(kwargs['coordinates']) >= 4, "Curve require at least 4 coordinates"
		super().__init__(**kwargs)

	@property
	@abstractmethod
	def draft(self):
		pass

# TODO: Allow more than 4 coordinates
class Bezier_curve(Curve):

	@property
	def draft(self):
		gx, gy = matrix.geometry(self.coordinates)

		t = 0
		draft = []
		while t < 1:
			x, y = (matrix.bezier(t) @ g for g in (gx, gy))
			draft.append((x, y))

			t += self.delta

		return draft


class Bspine_curve(Curve):
	@property
	def draft(self):
		i = 4
		draft = []
		while i <= len(self.coordinates):
			gx, gy = matrix.geometry(self.coordinates[i-4:i])

			cx, cy = (matrix.bspine() @ g for g in (gx, gy))
			dx, dy = (matrix.initial_differences(self.delta) @ c for c in (cx, cy))

			forward_differences = lambda d: [sum(d[i - 2:i]) for i in range(2, len(d)+2)]

			j = 0
			while j < 1.0:
				draft.append((dx[0], dy[0]))
				(dx, dy) = (forward_differences(d) for d in (dx+[0], dy+[0]))

				j += self.delta
			i += 1

		return draft
