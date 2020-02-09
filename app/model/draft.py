from core import __log__


class Draft:
	sketch = {
		'Dot': [],
		'Trace': []
	}

	def __getitem__(self, key):
		return self.sketch[key]

	def __add__(self, sketch):
		for key in sketch.keys():
			for scratch in sketch[key]:
				self.sketch[key].append(scratch)
		return self

	def __str__(self):
		return self.sketch.__str__()

	def keys(self):
		return self.sketch.keys()

	def per_coordinate(self, transformation):
		for key in self.keys():
			for i, scratch in enumerate(self[key]):
				transformed = [transformation(coordinate) for coordinate in scratch]

				if transformed != scratch:
					del self[key][i]

					if transformed:
						self[key].insert(i, transformed)

	def per_dot(self, transformation):
		self.transform('Dot', transformation)

	def per_trace(self, transformation):
		self.transform('Trace', transformation)

	def transform(self, key, transformation):
		sketch = self[key]

		i = 0
		while i < len(sketch):
			actual = sketch[i]
			transformed = transformation(actual)

			if transformed != actual:
				del sketch[i]

				if transformed:
					sketch.insert(i, transformed)
				else:
					continue
			i += 1

	def overwrite(self, key, i, transformed):
		if transformed != self[key][i]:
			del self[key][i]

			if transformed:
				self[key].insert(i, transformed)