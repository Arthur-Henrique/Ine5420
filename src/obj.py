import numpy as np

class Object:
    def __init__(self, name, type, color, coordenates):
        self.name = name
        self.type = type
        self.color = color
        self.coordenates = coordenates

    @property
    def origin(self):
        return self.coordenates[0]

    @property
    def center(self):
        return (
            sum(x / self.grade for x, _ in self.coordenates),
            sum(y / self.grade for _, y in self.coordenates)
        )

    @property
    def grade(self):
        return len(self.coordenates)

    # TODO: Remove logic from objects
    @property
    def homogenized_coordenates(self):
        coordenates = []
        for coordenate in self.coordenates:
            (x, y) = coordenate
            coordenates.append(np.array(([x, y, 1]), dtype=float))
        return coordenates

class Point(Object):
    def __init__(self, name, color, coordenates):
        super().__init__(name, "Point", color, coordenates);

    @property
    def x(self):
        return self.origin[0]

    @property
    def y(self):
        return self.origin[1]

class Line(Object):
    def __init__(self, name, color, coordenates):
        super().__init__(name, "Line", color, coordenates);

class Wireframe(Object):
    def __init__(self, name, color, coordenates):
        super().__init__(name, "Wireframe", color, coordenates);
