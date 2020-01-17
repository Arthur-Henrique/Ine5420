from unittest import TestCase
from app.model import Clipping

from core.log import __log__


class ClippingTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.clipping = Clipping((50, 50), (750, 750))

    def test_1(self):
        point = [(0, 0)]
        result = point @ self.clipping
        __log__("Outsider", point, "-", result, "\n")
        self.assertEqual([], result)

        point = [(100, 100)]
        result = point @ self.clipping
        # print("Insider", point, "-", result, "\n")
        self.assertEqual(point, result)

    def test_2(self):
        line = [(55, 5), (5, 55)]
        result = line @ self.clipping
        # print("Outsider", line, "-", result, "\n")
        self.assertEqual([None], result)

        line = [(50, 50), (100, 100)]
        result = line @ self.clipping
        # print("Totally in", line, "-", result, "\n")
        self.assertEqual(line, result)

        line = [(850, 100), (100, 100)]
        result = line @ self.clipping
        # print("In-and-out", line, "-", result, "\n")
        self.assertTrue((800, 100) in result)

        line = [(500, 0), (800, 1000)]
        result = line @ self.clipping
        # print("Through", line, "-", result, "\n")
        self.assertEqual(3, len(result))
        self.assertTrue(None in result)

    def test_3(self):
        wireframe = [(100, 100), (200, 400), (300, 600)]
        result = wireframe @ self.clipping
        # print("All-in", wireframe, "-", result, "\n")
        self.assertEqual(wireframe, result)

        wireframe = [(0, 0), (200, 400), (300, 600)]
        result = wireframe @ self.clipping
        # print("First out", wireframe, "-", result, "\n")
        self.assertEqual(4, len(result))
        self.assertIsNone(result[0])

        wireframe = [(100, 100), (1000, 400), (300, 600)]
        result = wireframe @ self.clipping
        # print("Middle out", wireframe, "-", result, "\n")
        self.assertEqual(5, len(result))
        self.assertIsNone(result[2])

        wireframe = [(100, 100), (100, 400), (3000, 0)]
        result = wireframe @ self.clipping
        # print("Last out", wireframe, "-", result, "\n")
        self.assertEqual(3, len(result))
        self.assertTrue(None is not result)

    def test_4(self):
        draft = [(500, 500), (400, 600), (700, 700), (100, 50)]
        result = draft @ self.clipping
        # print("All-in", draft, "-", result, "\n")
        self.assertEqual(draft, result)

        draft = [(500, 100), (815, -100), (900, 300), (500, 300)]
        result = draft @ self.clipping
        # print("Second out", draft, "-", result, "\n")
        self.assertEqual(5, len(result))
        self.assertEqual(None, result[2])

        draft = [(810, 50), (500, 500), (1000, 1000), (900, 500)]
        result = draft @ self.clipping
        # print("Loko", draft, "-", result, "\n")
        self.assertEqual(4, len(result))

    def test_5(self):
        draft = [(-121.82852795533461, 652.35724983379328), (218.23829999201484, -76.918416135030967),
         (570.09896810807174, 400.51623699636843), (690.12255444243044, 143.1248254779598)]
        result = draft @ self.clipping
        # print("***", draft, "-", result, "\n")

from app.clipping import Rectangle

class RectangleTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rectangle = Rectangle((50, 50, 750, 750))

    def test(self):
        line = [(55, 5), (5, 55)]
        # print("Outsider", line)
        # [self.assertTrue(externality) for (_, externality) in line @ self.rectangle]
        # print(line @ self.rectangle, "\n")

        line = [(5, 100), (100, 5)]
        # print("Passing by", line)
        # [self.assertFalse(externality) for (_, externality) in line @ self.rectangle]
        # print(line @ self.rectangle, "\n")

        line = [(850, 100), (100, 100)]
        # print("From inside", line)
        # [self.assertFalse(externality) for (_, externality) in line @ self.rectangle]
        # print(line @ self.rectangle, "\n")

        line = [(500, 500), (900, 0)]
        # print("From inside, double adjust", line)
        # [self.assertFalse(externality) for (_, externality) in line]
        # print(line @ self.rectangle, "\n")