from obj import *
import transformation
import numpy as np
import math


def init():
    global OBJECT_MANAGER
    global WINDOW
    global VIEWPORT
    global PROJECTIONS

    OBJECT_MANAGER = ObjectManager()
    PROJECTIONS = []

def project(change=""):
    for projection in PROJECTIONS:
        projection.refresh(change)

def normalize(point):
    (x, y) = point
    return np.array(([x, y, 1]), dtype=float)

class ObjectManager:
    id_counter = -1
    display_file = []

    def __init__(self):
        pass

    # TODO: Improve Object distinction algoritm
    def create(self, name, color, coordenates):
        object = None

        if len(coordenates) == 1:
            object = Point(name, color, coordenates)

        if len(coordenates) == 2:
            object = Line(name, color, coordenates)

        if len(coordenates) > 2:
            object = Wireframe(name, color, coordenates)

        self.register(object)
        return object

    def register(self, object):
        self.id_counter += 1
        object.id = self.id_counter

        self.display_file.append(object)
        project("display_file");

    def delete(self, id):
        for i in range(len(self.display_file)):
            if self.display_file[i].id == id:
                self.display_file.pop(i)
                break
        project("display_file");

    def clear(self):
        self.display_file = []
        project("display_file");

    def move(self, id, measure, direction, reference):
        object = self.get(id)

        if not reference:
            (dx, dy) = direction
        else:
            [dx, dy, _] = normalize(direction) @ transformation.rotate(reference)

        self.transform(object,
            transformation.translate(measure * dx, measure * dy)
        )

    def turn(self, id, measure, direction, reference):
        object = self.get(id)
        (rx,ry) = object.center if not reference else reference

        self.transform(object,
            transformation.translate(-rx, -ry) \
            @ transformation.rotate(math.radians(measure * direction[0])) \
            @ transformation.translate(rx, ry)
        )

    def zoom(self, id, measure, direction, reference):
        object = self.get(id)
        (rx,ry) = object.center if not reference else reference

        self.transform(object,
            transformation.translate(-rx, -ry) \
            @ transformation.scale(1 + measure/100 * direction[1]) \
            @ transformation.translate(rx, ry)
        )

    def transform(self, object, transformation):
        object.coordenates = list(
            (x, y) for [x, y, _] in list(
                hc @ transformation
                for hc in object.homogenized_coordenates
            )
        )
        project("object_transformation")

    def get(self, id):
        for object in self.display_file:
            if object.id == id:
                return object;

    def __iter__(self):
        return iter(self.display_file)


class Direction:
    UP = (0, -1)
    LEFT = (-1, 0)
    DOWN = (0, 1)
    RIGHT = (1, 0)

class Landscape:
    origin = None
    area = None
    angle = None
    scale = None

    def __init__(self, origin, area, angle, scale):
        self.origin = origin
        self.area = area
        self.angle = math.radians(angle)
        self.scale = scale

    @property
    def x(self):
        return self.origin[0]

    @property
    def y(self):
        return self.origin[1]

    @property
    def height(self):
        return self.area[0]

    @property
    def width(self):
        return self.area[1]

    @property
    def center(self):
        return (
            self.x + self.width/2,
            self.y + self.height/2
        )

class Window(Landscape):
    def __init__(self, origin, area, angle=0, scale=1):
        super().__init__(origin, area, angle, scale)

    def move(self, measure, direction):
        (dx, dy) = direction
        self.origin = (
            self.x + measure * dx,
            self.y + measure * dy
        )
        project("window_transformation")

    def turn(self, measure, direction):
        self.angle += math.radians(measure * direction[0])
        project("window_transformation")

    def zoom(self, measure, direction):
        self.scale *= 1 + measure/100 * direction[1]
        project("window_transformation")

    @property
    def perspective(self):
        (cx, cy) = self.center

        return transformation.translate(-cx, -cy) \
             @ transformation.scale(self.scale) \
             @ transformation.rotate(-self.angle) \
             @ transformation.translate(cx, cy) \
             @ transformation.translate(-self.x, -self.y)

class Viewport:
    def __init__(self):
        pass

    def ajust(self, coordenates):
        representation = []
        for coordenate in coordenates:
            [x, y, _] = normalize(coordenate) \
                @ WINDOW.perspective
            representation.append((x, y))
        return representation
