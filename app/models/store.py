import os
import re

from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import fields, validates, ValidationError, pre_load, post_load

from . import db, ma, Share


class Store(db.Model):
	__tablename__ = "stores"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), nullable=False)
	number = db.Column(db.Integer, nullable=False)
	descriptor = db.Column(db.String(64), nullable=False)
	lancou = db.Column(db.String(7), nullable=False)
	path = db.Column(db.String(128), unique=True, nullable=False)
	created = db.Column(db.TIMESTAMP, default=db.func.now(), nullable=False)
	modified = db.Column(db.TIMESTAMP, default=db.func.now(), nullable=False)
	share_id = db.Column(db.Integer, db.ForeignKey("shares.id"), nullable=False)
	shares = db.relationship("Share", backref="stores")

	def __init__(self, name, number, descriptor, lancou, path, share_id):
		self.name = name
		self.number = number
		self.descriptor = descriptor
		self.lancou = lancou
		self.path = path
		self.share_id = share_id

	def __repr__(self):
		return "<Store {}>".format(self.path)

	@hybrid_property
	def full_path(self):
		return os.path.join(self.shares.path, self.path)


class Store_Schema(ma.ModelSchema):
	class Meta:
		model = Store

	id = fields.Integer(dump_only=True)
	name = fields.String(required=True)
	number = fields.Integer(required=True)
	descriptor = fields.String(required=True)
	lancou = fields.String(required=True)
	path = fields.String()
	created = fields.DateTime(dump_only=True)
	modified = fields.DateTime(dump_only=True)
	share_id = fields.Integer(required=True, load_only=True)
	shares = ma.HyperlinkRelated("api.share")

	@pre_load
	def pre_validation(self, data):
		data = {k: v.strip() for k, v in data.items() if isinstance(v, str)}
		return data

	@post_load
	def post_validation(self, store):
		store.name = store.name.title()
		store.descriptor = store.descriptor.title()
		store.lancou = store.lancou.upper()
		if store.descriptor:
			store.path = "_".join([store.name, str(store.number), store.descriptor, store.lancou])
		else:
			store.path = "_".join([store.name, str(store.number), store.lancou])

		if Store.query.filter_by(name=store.name, number=store.number, descriptor=store.descriptor, lancou=store.lancou).all():
			raise ValidationError("Store already exists.", "error")

		share_path = Share.query.get(store.share_id)

		try:
			os.mkdir(os.path.join(share_path.path, store.path))
		except Exception as e:
			raise ValidationError(str(e), "error")

	@validates("name")
	def validate_name(self, value):
		if not value.isalpha():
			raise ValidationError("Invalid characters.")

	@validates("number")
	def validate_number(self, value):
		if not len(str(value)) == 5:
			raise ValidationError("Invalid length.")

	@validates("descriptor")
	def validate_descriptor(self, value):
		if value:
			if not re.match(r"^[a-zA-Z-\d]+$", value):
				raise ValidationError("Invalid characters.")

	@validates("lancou")
	def validate_lancou(self, value):
		if not re.match(r"^[a-zA-Z]{3}_[a-zA-Z]{3}$", value):
			raise ValidationError("Invalid lancou.")

	@validates('share_id')
	def validate_share_id(self, value):
		if not Share.query.get(value):
			raise ValidationError("Share doesn't exist.")
