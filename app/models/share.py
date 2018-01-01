from marshmallow import fields

from . import db, ma


class Share(db.Model):
	__tablename__ = "shares"

	id = db.Column(db.Integer, primary_key=True)
	path = db.Column(db.Text, unique=True, nullable=False)

	def __init__(self, path):
		self.path = path

	def __repr__(self):
		return "<Share {}>".format(self.path)


class Share_Schema(ma.ModelSchema):
	class Meta:
		model = Share

	id = fields.Integer(dump_only=True)
	path = fields.String(required=True)
