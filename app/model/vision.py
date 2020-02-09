from app.util import direction, normalize


class Vision:
	window = None

	def __init__(self, window):
		self.window = window

	def __rmatmul__(self, draft):
		draft.per_trace(self.transform)
		return draft

	def transform(self, line):
		forwardty = [self.define_forwardty(coordinate) for coordinate in line]

		if all(forwardty):
			return line
		elif any(forwardty):
			return self.clip(line.copy())
		else:
			return None

	def clip(self, line):
		[(i, origin)] = [
			(i, coordinate) for (i, coordinate) in enumerate(line)
			if self.define_forwardty(coordinate)
		]
		other = line[i - 1]

		[x, y, z, _] = normalize(origin) @ (direction([origin, other], self.window.z))

		return [origin, (x, y, z)]

	def define_forwardty(self, coordinate):
		(x, y, z) = coordinate
		return z >= self.window.z
