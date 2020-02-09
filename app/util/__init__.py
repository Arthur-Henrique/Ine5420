from app.util.matrix import *
from app.util.frame import *
import math


WORLD_CENTER = (0, 0, 0)


class Direction:
	UP = (0, -1, 0)
	LEFT = (-1, 0, 0)
	DOWN = (0, 1, 0)
	RIGHT = (1, 0, 0)