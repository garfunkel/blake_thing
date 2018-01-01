from abc import ABC, ABCMeta, abstractmethod

from .input import Base_Input, ValidationError

scripts = {}

class Script_Meta(type):
	def __init__(cls, name, bases, nmspc):
		super(Script_Meta, cls).__init__(name, bases, nmspc)
		if not name == "Script":
			scripts[cls.__name__] = cls
			scripts.pop(bases[0].__name__, None)
		cls.inputs = {}
		for name, obj in cls.__dict__.items():
			if issubclass(type(obj), Base_Input):
				cls.inputs[name] = obj


class _CombinedMeta(ABCMeta, Script_Meta): pass


class Script(ABC, metaclass=_CombinedMeta):
	name = None
	description = None

	def __init__(self, celery=None, logger=None, **kwargs):
		self.celery = celery
		self.logger = logger
		for name in self.inputs.keys():
			setattr(self, name, kwargs.get(name))

	@classmethod
	def validate(self, data):
		errors = {}
		for name, obj in self.inputs.items():
			if not obj.required and name in data.keys() and not data[name]:
				data[name] = None
				continue
			try:
				data[name] = obj._validate(data[name])
			except KeyError:
				if obj.required:
					errors[name] = "Required input not supplied"
				data[name] = None
			except ValidationError as e:
				errors[name] = str(e)
				data[name] = None
			except:
				raise
		return (data, errors)

	@classmethod
	def parse(self, data, celery=None, logger=None):
		return scripts[self.__name__](celery, logger, **data)

	@classmethod
	def to_dict(self):
		return {
			"id": self.__name__,
			"name": self.name,
			"description": self.description
		}

	@abstractmethod
	def run(self):
		pass

	def update_meta(self, meta):
		if self.celery:
			self.celery.update_state(state="PROGRESS", meta=meta)
