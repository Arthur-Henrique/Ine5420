import unittest

from app import domain
from app.model import Landscape
from app.model import Draft


class DraftTestCase(unittest.TestCase):
	landscape = Landscape((10, 10, 10))

	def test_landscape(self):
		for sketch in [
			{'Dot': [(10, 10, 10)]},
			{'Dot': [(30, 10, 90)]},
			{'Trace': [[(50, 50, 0), (200, 200, 0)]]},
			{'Trace': [[(100, 10, 0), (600, 40, 0)], [(600, 40, 0), (-50, 50, 0)]]}
		]:
			self.draft + sketch

		print(self.draft)

		self.draft @ self.landscape

		print(self.draft)

	def test_polygon(self):
		c = domain.create(
			name='c',
			type='Chain',
			color=(0, 0, 1),
			coordinates=[(100, 100, 10), (100, 400, 10), (400, 400, 10), (400, 100, 10)]
		)

		p = domain.create(
			name='p',
			type='Polygon',
			color=(0, 0, 1),
			coordinates=[(100, 100, 10), (100, 400, 10), (400, 400, 10), (400, 100, 10)]
		)

		print(c.draft)
		print(p.draft)

	def test_vision(self):
		l = domain.create(
			name='l',
			type='Line',
			color=(0, 0, 1),
			coordinates=[(50, 50, 30), (50, 50, 5)]
		)

		draft = Draft() + l.draft

		draft @ self.landscape

		print(draft)

