from app.model import Frame
from app.util import direction, normalize


class Vision(Frame):

	def __init__(self, limit):
		super().__init__()
		self.limit = limit

	def __rmatmul__(self, draft):
		draft.per_trace(self.transform)
		return draft

	def transform(self, coordinates, **kwargs):
		forwardty = [self.define_forwardty(coordinate) for coordinate in coordinates]

		if all(forwardty):
			return coordinates
		elif any(forwardty):
			return self.clip(coordinates)
		else:
			return None

	def clip(self, line):
		[(i, origin)] = [
			(i, coordinate) for (i, coordinate) in enumerate(line)
			if self.define_forwardty(coordinate)
		]
		other = line[i - 1]

		[x, y, z, _] = normalize(origin) @ (direction([origin, other], self.limit))

		return [origin, (x, y, z)]

	def define_forwardty(self, coordinate):
		(x, y, z) = coordinate
		return z >= self.limit
