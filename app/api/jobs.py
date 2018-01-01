from flask import current_app, make_response, jsonify, request
from flask_restful import Resource

from . import api

class Jobs_API(Resource):
	def get(self):
		return make_response(jsonify({"None": "Meow"}), 201)


class Job_API(Resource):
	def get(self):
		return make_response(jsonify({"None": "Meow"}), 201)
