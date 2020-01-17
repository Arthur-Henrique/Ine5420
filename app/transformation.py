from numpy import array, cos, sin


def base():
    return array((
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ), dtype=float)

def normalize(coordenates):
    return [array(([x, y, 1]), dtype=float) for (x, y) in coordenates]

def translate(x, y):
    return array((
        [1, 0, 0],
        [0, 1, 0],
        [x, y, 1]
    ), dtype=float)

def rotate(angle):
    c = cos(angle)
    s = sin(angle)

    return array((
        [c, -s, 0],
        [s, c, 0],
        [0,   0,   1]
    ), dtype=float)

def scale(scale):
    return array((
        [scale, 0, 0],
        [0, scale, 0],
        [0,   0,   1]
    ), dtype=float)
