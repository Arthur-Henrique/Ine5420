from app import domain
from app.util import math, normalize, translate, scale, rotate
from core import __log__, __project__


class ObjectManager:
	def move(self, id, measure, direction, reference):
		object = domain.get(id)

		if not reference:
			(dx, dy) = direction
		else:
			[[dx, dy, _]] = normalize([direction]) @ rotate(reference)

		self.transform(object, translate(measure * dx, measure * dy))

	def turn(self, id, measure, direction, reference):
		object = domain.get(id)
		(rx, ry) = reference if reference else object.center

		self.transform(object,
						translate(-rx, -ry) \
						@ rotate(math.radians(measure * direction[0])) \
						@ translate(rx, ry)
		)

	def zoom(self, id, measure, direction, reference):
		object = domain.get(id)
		(rx, ry) = reference if reference else object.center

		self.transform(object,
						translate(-rx, -ry) \
						@ scale(1 + measure / 100 * direction[1]) \
						@ translate(rx, ry)
		)

	def transform(self, object, transformation):
		object.coordinates = [
			(x, y) for [x, y, _] in [
				coordinate @ transformation
				for coordinate in normalize(object.coordinates)
			]
		]
		__project__("object_transformation")
