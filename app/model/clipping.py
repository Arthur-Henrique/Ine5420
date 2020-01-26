from app.util import Rectangle


class Clipping(Rectangle):

	def __rmatmul__(self, coordinates):

		cohen_sutherland_list = [
			(coordinate, self.define_externality(coordinate))
			for coordinate
			in coordinates
		]

		i = 0
		while i < len(cohen_sutherland_list):
			if i == 0:
				if len(cohen_sutherland_list) == 1 and cohen_sutherland_list[0][1]:
					return []
			else:
				[previous, actual] = cohen_sutherland_list[i - 1:i + 1]
				line = [previous[0], actual[0]]

				if sum(previous[1]) & sum(actual[1]) != 0:
					del cohen_sutherland_list[i - 1]
					i -= 1

					if i == len(cohen_sutherland_list) - 1:
						del cohen_sutherland_list[i]

				elif sum(previous[1]) | sum(actual[1]) != 0:
					clipped = self.clip(line.copy())

					for j, adjusted in enumerate(clipped):
						target = line[j]

						if adjusted != target:
							if j == 0:
								cohen_sutherland_list[i - 1] = (None, [])
							elif i == len(cohen_sutherland_list) - 1:
								del cohen_sutherland_list[i]

							if not self.define_externality(adjusted):
								cohen_sutherland_list.insert(i, (adjusted, []))
								i += 1
			i += 1

		return [coordinate for (coordinate, _) in cohen_sutherland_list]

	def clip(self, line):
		for i in [0, 1]:
			(x0, y0) = line[i]
			(x1, y1) = line[i - 1]

			_x = (x1 - x0)
			_y = (y1 - y0)

			if x0 < self.left or x0 > self.right:
				limit = self.left if x0 < self.left else self.right
				m = _y / _x

				y0 = y0 + m * (limit - x0)
				x0 = limit

			if y0 < self.bottom or y0 > self.top:
				limit = self.bottom if y0 < self.bottom else self.top
				m = _x / _y

				x0 = x0 + m * (limit - y0)
				y0 = limit

			if (x0, y0) != line[i]:
				line[i] = (x0, y0)

		return line

	def define_externality(self, coordinate):

		(x, y) = coordinate

		externality = []

		if x < self.left:
			externality.append(Externality.LEFT)
		elif x > self.right:
			externality.append(Externality.RIGTH)

		if y < self.bottom:
			externality.append(Externality.BELLOW)
		elif y > self.top:
			externality.append(Externality.ABOVE)

		return externality


class Externality:
	INSIDE = 0
	LEFT = 1
	RIGTH = 2
	BELLOW = 4
	ABOVE = 8
