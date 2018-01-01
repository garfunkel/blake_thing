import os

from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import fields

from . import db, ma


class Job(db.Model):
	__tablename__ = "jobs"

	id = db.Column(db.Integer, primary_key=True)
	task_id = db.Column(db.String(36), nullable=False)
	created = db.Column(db.TIMESTAMP, default=db.func.now())

	def __init__(self):
		pass

	def __repr__(self):
		return "<Job {}>".format(self.task_id)

	@hybrid_property
	def path(self):
		return os.path.join(current_app.config["BLAKE_JOB_DIR"], self.task_id)


class Job_Schema(ma.ModelSchema):
	class Meta:
		model = Job
