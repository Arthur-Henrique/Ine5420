class Externality:
    INSIDE = 0
    LEFT = 1
    RIGTH = 2
    BELLOW = 4
    ABOVE = 8

class Rectangle:
    def __init__(self, draft):
        x, y, width, height = draft

        self.left = x
        self.right = x + width
        self.bottom = y
        self.top = y + height

    def __rmatmul__(self, line):
        for i in [0, 1]:
            (x0, y0) = line[i]
            (x1, y1) = line[i-1]

            _x = (x1 - x0)
            _y = (y1 - y0)

            # unajustable = False

            if x0 < self.left or x0 > self.right:
                limit = self.left if x0 < self.left else self.right
                m = _y / _x

                # p = y1 + m * (limit - x1)
                # if self.left <= p and p <= self.right:
                y0 = y0 + m * (limit - x0)
                x0 = limit
                # else:
                #     unajustable = True

            if y0 < self.bottom or y0 > self.top:
                limit = self.bottom if y0 < self.bottom else self.top
                m = _x / _y

                # p = y1 + m * (limit - x1)
                # if self.bottom <= p and p <= self.top:
                x0 = x0 + m * (limit - y0)
                y0 = limit
                # else:
                #     unajustable = True

            if (x0, y0) != line[i]:
                line[i] = (x0, y0)
            # elif unajustable:
            #     return (None, None)

        return line

    def define_externality(self, coordenate):

        (x, y) = coordenate

        externality = []

        if x < self.left:
            externality.append(Externality.LEFT)
        elif x > self.right:
            externality.append(Externality.RIGTH)

        if y < self.bottom:
            externality.append(Externality.BELLOW)
        elif y > self.top:
            externality.append(Externality.ABOVE)

        return externality

def Cohen_Sutherland(coordenates, rectangle):
    rectangle = Rectangle(rectangle)

    cohen_sutherland_list = [
        (coordenate, rectangle.define_externality(coordenate))
        for coordenate
        in coordenates
    ]

    i = 0
    while i < len(cohen_sutherland_list):
        if i == 0:
            if len(cohen_sutherland_list) == 1 and rectangle.define_externality(coordenates[0]):
                return []
        else:
            [previous, actual] = cohen_sutherland_list[i-1:i+1]
            line = [previous[0], actual[0]]

            if sum(previous[1]) & sum(actual[1]) != 0:
                del cohen_sutherland_list[i-1]
                i -= 1

                if i == len(cohen_sutherland_list)-1:
                    del cohen_sutherland_list[i]

            elif sum(previous[1]) | sum(actual[1]) != 0:
                for j, adjusted in enumerate(line.copy() @ rectangle):
                    target = line[j]

                    if adjusted != target:
                        if j == 0:
                            cohen_sutherland_list[i-1] = (None, [])
                        elif i == len(cohen_sutherland_list)-1:
                            del cohen_sutherland_list[i]

                        if not rectangle.define_externality(adjusted):
                            cohen_sutherland_list.insert(i, (adjusted, []))
                            i += 1
        i += 1

    return [coordenate for (coordenate, _) in cohen_sutherland_list]