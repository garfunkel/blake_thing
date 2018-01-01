from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_security import Security, SQLAlchemyUserDatastore
from celery import Celery
from flask_socketio import SocketIO
from flask_redis import Redis

from config import config, Config


db = SQLAlchemy()
ma = Marshmallow()
mail = Mail()
security = Security()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
socketio = SocketIO()
redis = Redis()


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])

	db.init_app(app)
	ma.init_app(app)
	mail.init_app(app)

	from .models.userrole import User, Role
	user_datastore = SQLAlchemyUserDatastore(db, User, Role)
	security.init_app(app, user_datastore)

	celery.conf.update(app.config)

	redis.init_app(app)

	socketio.init_app(app)	# TODO: Temporary... move to better location...
	from .sockets import JobsNamespace
	socketio.on_namespace(JobsNamespace('/jobs'))

	from .main import main_bp as main_blueprint
	app.register_blueprint(main_blueprint)

	from .api import api_bp as api_blueprint
	app.register_blueprint(api_blueprint, url_prefix="/api")

	from .admin import admin_bp as admin_blueprint
	app.register_blueprint(admin_blueprint, url_prefix="/admin")

	return app
