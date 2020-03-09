from abc import abstractmethod


class Frame:

	@abstractmethod
	def __rmatmul__(self, draft):
		pass

	@abstractmethod
	def transform(self, **kwargs):
		pass


