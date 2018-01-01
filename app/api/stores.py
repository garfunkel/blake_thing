from flask import current_app, request, make_response, jsonify
from flask_restful import Resource

from . import api
from app import db
from app.models.store import Store, Store_Schema, Share


class Stores_API(Resource):
	def get(self):
		stores = Store.query.all()
		return Store_Schema(many=True, only=('id', 'name', 'number', 'descriptor', 'lancou')).jsonify(stores)

	def post(self):
		data = request.get_json(force=True)
		result = Store_Schema().load(data)
		if result.errors:
			return make_response(jsonify(result.errors), 400)

		result.data.shares = Share.query.get(data["share_id"])

		db.session.add(result.data)
		db.session.commit()

		return make_response(Store_Schema().jsonify(result.data), 201)


class Store_API(Resource):
	def get(self, id):
		store = Store.query.get(id)

		if not store:
			return make_response(jsonify({"error": "Resource not found"}), 404)

		return make_response(Store_Schema().jsonify(store), 200)
