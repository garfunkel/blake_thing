from flask_security import UserMixin, RoleMixin

from . import db


roles_users = db.Table('roles_users',
	db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')),
	db.Column('user_id', db.Integer(), db.ForeignKey('users.id')))


class Role(db.Model, RoleMixin):
	__tablename__ = "roles"
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.Text, unique=True)
	description = db.Column(db.Text)

	def __init__(self, name, description):
		self.name = name
		self.description = description
		

class User(db.Model, UserMixin):
	__tablename__ = "users"
	
	id = db.Column(db.Integer(), primary_key=True)
	email = db.Column(db.Text, unique=True)
	password = db.Column(db.Text)
	active = db.Column(db.Boolean())
	roles = db.relationship('Role', secondary=roles_users,
		backref = db.backref('users', lazy='dynamic'))
