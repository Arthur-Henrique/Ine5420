import numpy as np

def base():
    return np.array((
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ), dtype=float)

def translate(x, y):
    return np.array((
        [1, 0, 0],
        [0, 1, 0],
        [x, y, 1]
    ), dtype=float)

def rotate(angle):
    cos = np.cos(angle)
    sin = np.sin(angle)

    return np.array((
        [cos, -sin, 0],
        [sin, cos, 0],
        [0,   0,   1]
    ), dtype=float)

def scale(scale):
    return np.array((
        [scale, 0, 0],
        [0, scale, 0],
        [0,   0,   1]
    ), dtype=float)
