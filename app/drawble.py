class Drawable:
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
            sum(x for x, _ in self.coordenates) / self.grade,
            sum(y for _, y in self.coordenates) / self.grade
        )

    @property
    def grade(self):
        return len(self.coordenates)

    def __str__(self):
        return f"""
            {self.name}, {self.type}
            {self.coordenates}
        """

class Point(Drawable):
    def __init__(self, name, color, coordenates):
        super().__init__(name, "Point", color, coordenates);

    @property
    def x(self):
        return self.origin[0]

    @property
    def y(self):
        return self.origin[1]

class Line(Drawable):
    def __init__(self, name, color, coordenates):
        super().__init__(name, "Line", color, coordenates);

class Wireframe(Drawable):
    def __init__(self, name, color, coordenates):
        super().__init__(name, "Wireframe", color, coordenates);
