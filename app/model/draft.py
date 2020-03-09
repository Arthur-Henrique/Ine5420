

class Draft:
	sketch = {
		'Dot': [],
		'Trace': [],
		'Face': []
	}

	def __getitem__(self, key):
		return self.sketch[key]

	def __add__(self, sketch):
		for key in sketch.keys():
			for scribble in sketch[key]:
				self.sketch[key].append(scribble)
		return self

	def __str__(self):
		return self.sketch.__str__()

	def keys(self):
		return self.sketch.keys()

	def per_coordinate(self, transformation):
		for key in self.keys():
			for i, scribble in enumerate(self[key]):
				coordinates, color = scribble.values()
				transformed = [transformation(coordinate) for coordinate in coordinates]

				if transformed != coordinates:
					del self[key][i]

					if transformed:
						self[key].insert(i, dict(
							coordinates=transformed,
							color=color
						))

	def per_dot(self, transformation):
		self.transform('Dot', transformation)

	def per_trace(self, transformation):
		self.transform('Trace', transformation)

	def per_face(self, transformation):
		self.transform('Face', transformation)

	def transform(self, key, transformation):
		sketch = self[key]

		i = 0
		while i < len(sketch):
			coordinates, color = sketch[i].values()
			transformed = transformation(coordinates=coordinates, color=color)

			if transformed != coordinates:
				del sketch[i]

				if transformed:
					sketch.insert(i, dict(
						coordinates=transformed,
						color=color
					))
				else:
					continue
			i += 1

	def overwrite(self, key, i, transformed):
		if transformed != self[key][i]:
			del self[key][i]

			if transformed:
				self[key].insert(i, transformed)