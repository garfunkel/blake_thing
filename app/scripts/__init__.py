import os
import sys
import re
import importlib
import inspect
import pathlib

from flask import current_app

from .script import Script, scripts
from .input import Boolean_Input, String_Input, Choice_Input, File_Input


def load_scripts():
	files = os.listdir(current_app.config["BLAKE_SCRIPT_DIR"])

	for i in files:
		if i.startswith(".") or not i.endswith(".py"):
			continue

		name= "app.scripts.Scripts_Dir.{}".format(i.split('.')[0])

		try:
			if name in sys.modules:
				module = importlib.reload(sys.modules[name])
			else:
				module = importlib.import_module(name)
			for name, obj in inspect.getmembers(module, inspect.isclass):
				if not issubclass(obj, Script):
					continue
				if Script.__name__ == obj.__name__:
					continue
		except Exception as e:
			print(e)
