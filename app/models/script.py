import os
from enum import Enum
from hashlib import md5
from shutil import copy

from marshmallow import fields, validates, ValidationError, post_load

from . import db, ma


class Script(db.Model):
	__tablename__ = "scripts"

	name = db.Column(db.Text, primary_key=True)
	path = db.Column(db.Text, nullable=False)

	def __init__(self, name, path):
		self.name = name
		self.path = path

	def __repr__(self):
		return "<Script {}>".format(self)


class Script_Schema(ma.ModelSchema):
	class Meta:
		model = Script

	name = fields.String(required=True)
	path = fields.String(required=True)
	

class Script_Version(db.Model):
	__tablename__ = "script_versions"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, nullable=False)
	version = db.Column(db.Float, nullable=False)
	checksum = db.Column(db.String(32), nullable=False)
	created = db.Column(db.TIMESTAMP, default=db.func.now())	
	
	def __init__(self, name, version, checksum, script_id):
		self.name = name
		self.version = version
		self.checksum = checksum
		self.script_id = script_id

	def __repr__(self):
		return "<Script_Version {}>".format(self)


class Script_Version_Schema(ma.ModelSchema):
	class Meta:
		model = Script_Version

	id = fields.Integer(dump_only=True)
	name = fields.String(required=True)
	version = fields.Float(required=True)
	checksum = fields.String(dump_only=True)
	created = fields.DateTime(dump_only=True)

	@post_load
	def create_version(self, data):
		data["checksum"] = md5(open(data["name"], 'rb').read()).hexdigest()
		return Script(**data)		

	@validates("name")
	def validate_path(self, value):
		if not os.path.exists(value):
			raise ValidationError("Path doesn't exist.")
		if not os.access(value, os.R_OK):
			raise ValidationError("Read permission required.")
