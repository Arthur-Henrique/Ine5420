from app.domain.drawable import Drawable, Geometric
from app.domain.form import *
from app.domain.loader import Loader
from core import __project__, __log__

global ID_COUNTER
global DISPLAY_FILE
global LOADER

ID_COUNTER = 0
DISPLAY_FILE = []


def create(type, **kwargs):
	shape = {
		'Point': Point,
		'Line': Line,
		'Chain': Chain,
		'Polygon': Polygon,
		'Face': Face,
		'Bezier_curve': BezierCurve,
		'BSpine_curve': BSpineCurve,
		'Bezier_surface': BezierSurface,
		'BSpine_surface': BSpineSurface
	}[type](**kwargs)

	register(shape)

	return shape


def register(shape):
	global ID_COUNTER
	ID_COUNTER += 1
	shape.id = ID_COUNTER

	global DISPLAY_FILE
	DISPLAY_FILE.append(shape)

	__log__(new_object=shape)
	__project__("display_file")


def get(id):
	for drawable in DISPLAY_FILE:
		if drawable.id == id:
			return drawable


def delete(id):
	global DISPLAY_FILE

	i = 0
	while i < len(DISPLAY_FILE):
		if DISPLAY_FILE[i].id == id:
			DISPLAY_FILE.pop(i)
			break
		i += 1

	__log__(object_deleted=id)
	__project__("display_file")


def describe(id):
	__log__(object=get(id))


def load(path):
	Loader().load(path)
	__log__(file_loaded=path)
	__project__("display_file")
