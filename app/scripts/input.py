from abc import ABC, abstractmethod


class ValidationError(Exception):
	def __init__(self, *args, **kwargs):
		Exception.__init__(self, *args, **kwargs)


class Base_Input(ABC):
	def __init__(self, name, help, required=True, default=""):
		self.name = name
		self.help = help
		self.required = required
		self.default = default

	@abstractmethod
	def _validate(self, value):
		pass

	def _parse(self, value):
		return self._validated(value)

	def to_dict(self):
		return {
			"type": self.__class__.__name__,
			"name": self.name,
			"help": self.help,
			"required": self.required,
			"default": self.default
		}


class Boolean_Input(Base_Input):
	true_values = [True, "True", "true", 'T', 't']
	false_values = [False, "False", "false", 'F', 'f']

	def _validate(self, value):
		if value in self.true_values:
			return True
		elif value in self.false_values:
			return False
		raise ValidationError("Not a valid Boolean.")


class String_Input(Base_Input):
	def _validate(self, value):
		if value is None or not value:
			raise ValidationError("Not a valid String.")
		return value


class Choice_Input(Base_Input):
	def __init__(self, name, help, choices, required=True, default=""):
		if type(choices) == list:
			self.choices = {v: v for v in choices} # I was lazy :P TODO: Fix this...
		else:
			self.choices = {str(k): str(v) for k, v in choices.items()}
		super(Choice_Input, self).__init__(name, help, required, default)

	def _validate(self, value):
		if value in self.choices.keys():
			return value
		raise ValidationError("Not a valid Choice.")

	def to_dict(self):
		return {**super(Choice_Input, self).to_dict(), "choices": self.choices}


class File_Input(Base_Input):
	def _validate(self, value):
		pass
