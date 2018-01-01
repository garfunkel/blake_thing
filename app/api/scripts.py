import os
import logging

from flask import current_app, make_response, jsonify, request
from flask_restful import Resource

from . import api
from app.scripts import scripts, load_scripts
from app.tasks import runScript


class Scripts_API(Resource):
	def get(self):
		load_scripts()

		data = []

		for script in scripts.values():
			data.append(script.to_dict())

		return make_response(jsonify(data), 201)


class Script_API(Resource):
	def get(self, name):
		load_scripts()

		try:
			script = scripts[name]
		except:
			return make_response(jsonify({"error": "Resource not found"}), 404)

		data = {}

		for name, input in script.inputs.items():
			data[name] = input.to_dict()

		return make_response(jsonify(data), 201)


	def post(self, name):
		try:
			script = scripts[name]
		except:
			return make_response(jsonify({"error": "Resource not found"}), 404)

		data = request.get_json(force=True)

		data, errors = script.validate(data)
		if errors:
			print(errors)
			return make_response(jsonify(errors), 400)

		# Start job....
		running = runScript.delay(name, data)

		return make_response(jsonify({"job": "123"}), 201)
