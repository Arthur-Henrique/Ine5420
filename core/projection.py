from abc import abstractmethod

global PROJECTIONS
PROJECTIONS = []


def __project__(*args, **kwargs):
	for projection in PROJECTIONS:
		projection.refresh(*args, **kwargs)

class Projection():
	def __init__(self):
		PROJECTIONS.append(self)

	@abstractmethod
	def refresh(self, *args, **kwargs):
		pass
