from app.drawble import *
from app.transformation import *
from app.clipping import Cohen_Sutherland

from core.log import __log__
from core.projection import __project__

import math
from abc import abstractmethod

#----------------------------------------------------------

def init():
    global OBJECT_MANAGER
    global WINDOW
    global VIEWPORT
    global CLIPPING

    OBJECT_MANAGER = ObjectManager()

#----------------------------------------------------------

class ObjectManager:
    id_counter = 0
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

        self.id_counter += 1
        object.id = self.id_counter

        self.register(object)

        __log__(log=object)

        return object

    def register(self, object):


        self.display_file.append(object)
        __project__("display_file");

    def delete(self, id):
        for i in range(len(self.display_file)):
            if self.display_file[i].id == id:
                self.display_file.pop(i)
                break
        __project__("display_file");

    def clear(self):
        self.display_file = []
        __project__("display_file");

    def move(self, id, measure, direction, reference):
        object = self.get(id)

        if not reference:
            (dx, dy) = direction
        else:
            [[dx, dy, _]] = normalize([direction]) @ rotate(reference)

        self.transform(object,
            translate(measure * dx, measure * dy)
        )

    def turn(self, id, measure, direction, reference):
        object = self.get(id)
        (rx, ry) = object.center if not reference else reference

        self.transform(object,
            translate(-rx, -ry) \
            @ rotate(math.radians(measure * direction[0])) \
            @ translate(rx, ry)
        )

    def zoom(self, id, measure, direction, reference):
        object = self.get(id)
        (rx, ry) = object.center if not reference else reference

        self.transform(object,
            translate(-rx, -ry) \
            @ scale(1 + measure/100 * direction[1]) \
            @ translate(rx, ry)
        )

    def transform(self, object, transformation):
        object.coordenates = [
                (x, y) for [x, y, _] in [
                n @ transformation
                for n in normalize(object.coordenates)
            ]
        ]
        __project__("object_transformation")

    def get(self, id):
        for object in self.display_file:
            if object.id == id:
                return object;

    def __iter__(self):
        return iter(self.display_file)

    def describe(self, id):
        object = self.get(id)
        print(object)

        representation = object.coordenates
        for landscape in [VIEWPORT, WINDOW, CLIPPING]:
            representation @= landscape
            print("         ", representation)

#----------------------------------------------------------

class Direction:
    UP = (0, -1)
    LEFT = (-1, 0)
    DOWN = (0, 1)
    RIGHT = (1, 0)

class Landscape:
    origin = None
    area = None

    def __init__(self, origin, area):
        self.origin = origin
        self.area = area

    @property
    def x(self):
        return self.origin[0]

    @property
    def y(self):
        return self.origin[1]

    @property
    def width(self):
        return self.area[0]

    @property
    def height(self):
        return self.area[1]

    @property
    def center(self):
        return (
            self.x + self.width/2,
            self.y + self.height/2
        )

    @property
    def end(self):
        return (
            self.x + self.width,
            self.y + self.height
        )

    @property
    def vertices(self):
        return (
            self.origin,
            (self.x + self.width, self.y),
            self.end,
            (self.x, self.y + self.height)
        )

    @property
    def rectangle(self):
        return (*self.origin, *self.area)

    @abstractmethod
    def __rmatmul__(self, coordenates):
        return


class Window(Landscape):
    angle = None
    scale = None

    def __init__(self, origin, area, angle=0, scale=1):
        super().__init__(origin, area)

        self.angle = math.radians(angle)
        self.scale = scale

    def move(self, measure, direction):
        (dx, dy) = direction
        [dx, dy, _] = [dx, dy, 1] @ rotate(self.angle)

        self.origin = (
            self.x + measure * dx,
            self.y + measure * dy
        )
        __project__("window_transformation")

    def turn(self, measure, direction):
        self.angle += math.radians(measure * direction[0])
        __project__("window_transformation")

    def zoom(self, measure, direction):
        self.scale *= 1 + measure/100 * direction[1]
        __project__("window_transformation")

    def __rmatmul__(self, coordenates):
        (cx, cy) = self.center

        representation = []
        for coordenate in normalize(coordenates):
            [x, y, _] = coordenate \
                        @ translate(-cx, -cy) \
                        @ scale(self.scale) \
                        @ rotate(-self.angle) \
                        @ translate(cx, cy) \
                        @ translate(-self.x, -self.y)

            representation.append((x, y))
        return representation

class Viewport(Landscape):
    def __init__(self, origin, area):
        super().__init__(origin, area)

    def __rmatmul__(self, coordenates):
        representation = []
        for (x, y) in coordenates:

            x = self.x + (x - WINDOW.x) * self.width / WINDOW.width
            y = self.y + (y - WINDOW.y) * self.height / WINDOW.height

            representation.append((x, y))
        return representation

class Clipping(Landscape):
    def __init__(self, origin, area):
        super().__init__(origin, area)

    def __rmatmul__(self, coordenates):
        return Cohen_Sutherland(coordenates, self.rectangle)
