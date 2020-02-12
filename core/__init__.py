from core.log import __log__
from core.projection import Projection, __project__

def __require__(requirement, message, *args):
	violation = []

	for arg in args:
		if not requirement(arg):
			violation.append(arg + ': ' + message)

	assert not violation, violation
