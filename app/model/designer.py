from app import domain
from app.model import Draft
from app.util import math, normalize, translate, scale, rotate
from core import __log__, __project__


class Designer:
	def move(self, id, measure, direction, reference):
		object = domain.get(id)

		if not reference:
			(dx, dy, _) = direction
		else:
			[dx, dy, *_] = normalize(direction) @ rotate(reference)

		transform(object, translate(measure * dx, measure * dy, 0))
		# __project__('log', object_movement=(id, measure, reference))

	def turn(self, id, measure, direction, reference, axis):
		object = domain.get(id)
		(rx, ry, _) = reference if reference else object.center

		transform(object,
						translate(-rx, -ry, 0) \
						@ rotate(math.radians(measure * direction[0]), axis) \
						@ translate(rx, ry, 0)
		)

	def zoom(self, id, measure, direction, reference):
		object = domain.get(id)
		(rx, ry, _) = reference if reference else object.center

		transform(object,
						translate(-rx, -ry, 0) \
						@ scale(1 + measure / 100 * direction[1]) \
						@ translate(rx, ry, 0)
		)

	@property
	def draft(self):
		draft = Draft()

		for drawable in domain.DISPLAY_FILE:
			draft + drawable.draft

		return draft


def transform(object, transformation):
	object.coordinates = [
		(x, y, z) for [x, y, z, _] in [
			normalize(coordinate) @ transformation
			for coordinate in object.coordinates
		]
	]
	__project__("object_transformation")