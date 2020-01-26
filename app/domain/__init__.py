from app.domain.drawble import Drawable
from app.domain.basic import Dot, Trace, Wireframe
from app.domain.curve import Bezier_curve, Bspine_curve
from core import __project__

global ID_COUNTER
global DISPLAY_FILE

ID_COUNTER = 0
DISPLAY_FILE = []


def create(**kwargs):
	object = {
		'Dot': Dot,
		'Trace': Trace,
		'Wireframe': Wireframe,
		'Bezier_curve': Bezier_curve,
		'Bspine_curve': Bspine_curve
	}[kwargs['type']](**kwargs)

	register(object)


def register(object):
	global ID_COUNTER
	ID_COUNTER += 1
	object.id = ID_COUNTER

	global DISPLAY_FILE
	DISPLAY_FILE.append(object)

	__project__("display_file", "log", new_object=object)


def get(id):
	return next(object for object in DISPLAY_FILE if object.id == id)


def delete(id):
	[DISPLAY_FILE.pop(i) for i in range(len(DISPLAY_FILE)) if DISPLAY_FILE.get(i).id == id]
	__project__("display_file")


def describe(id):
	__project__("log", object=get(id))
