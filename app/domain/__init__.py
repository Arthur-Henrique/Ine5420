from app.domain.drawble import Drawable
from app.domain.shape import *
from app.domain.loader import Loader
from core import __project__

global ID_COUNTER
global DISPLAY_FILE

ID_COUNTER = 0
DISPLAY_FILE = []


def create(**kwargs):
	object = {
		'Point': Point,
		'Line': Line,
		'Chain': Chain,
		'Polygon': Polygon,
		'Bezier_curve': BezierCurve,
		'BSpine_curve': BSpineCurve,
		'Bezier_surface': BezierSurface,
		'BSpine_surface': BSpineSurface
	}[kwargs['type']](**kwargs)

	register(object)

	return object


def register(object):
	global ID_COUNTER
	ID_COUNTER += 1
	object.id = ID_COUNTER

	global DISPLAY_FILE
	DISPLAY_FILE.append(object)

	__project__("display_file", "log", new_object=object)


def get(id):
	for drawable in DISPLAY_FILE:
		if drawable.id == id:
			return drawable


def delete(id):
	global DISPLAY_FILE
	[DISPLAY_FILE.pop(i) for i in range(len(DISPLAY_FILE)) if DISPLAY_FILE[i].id == id]
	__project__("display_file")


def describe(id):
	__project__("log", object=get(id))


def load(*args):
	Loader().load(*args)
