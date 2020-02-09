class AllArgsInit:
	required = None

	def __init__(self, required=False):
		self.required = required

	def __call__(self, cls):
		def constructor(obj, *args, **kwargs):
			nonPresentArgs = []

			@forAttr(cls=cls)
			def setAttributes(obj, __attr__, *args, **kwargs):
				try:
					setattr(obj, __attr__, kwargs[__attr__])
				except KeyError:
					nonPresentArgs.append(__attr__)

			setAttributes(obj, *args, **kwargs)

			if self.required and nonPresentArgs:
				raise ValueError(str(nonPresentArgs) + ' are required')

		setattr(cls, "__init__", constructor)
		return cls


class SuperInit:

	def __init__(self):
		pass

	def __call__(self, cls):
		def init(obj, *args, **kwargs):
			super().__init__(*args, **kwargs)

		setattr(cls, "__init__", init)
		return cls


def forAttr(cls):
	def decorator(func):
		def result(self=None, *args, **kwargs):
			for __attr__ in [
				__attr__ for __attr__ in dir(cls)
				if not __attr__.startswith('__')
				   and not callable(getattr(cls, __attr__))
			]:
				func(self, __attr__, *args, **kwargs)

		return result

	return decorator

def at(context):
	class At:
		func = context
		def __rmatmul__(self, arg):
			return self.func(arg)

	return At()
