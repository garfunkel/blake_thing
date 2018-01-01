from flask import current_app
from flask_restful import Resource

from . import api
from app.models import Share, Share_Schema


class Shares_API(Resource):
	def get(self):
		shares = Share.query.all()
		return Share_Schema(many=True).jsonify(shares)


class Share_API(Resource):
	def get(self, id):
		store = Share.query.get(id)
		return Share_Schema().jsonify(store)
