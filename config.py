from kombu import Queue, Exchange

class Config:
	# Blake
	BLAKE_JOB_DIR = "/home/harry/Documents/blake_thing/Jobs"
	BLAKE_SCRIPT_DIR = "/home/harry/Documents/blake_thing/app/scripts/Scripts_Dir"
	BALKE_SCRIPT_VERSIONS = "/home/harry/Documents/blake_thing/app/scripts/Scripts_Versions"
	BLAKE_MAX_STORE_DAYS = 1

	# Flask
	SECRET_KEY = "Meow"

	# Flask-SQLAlchemy
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Flask-Security
	SECURITY_REGISTERABLE = True
	SECURITY_PASSWORD_SALT = "Meow"
	SECURITY_POST_LOGOUT_VIEW = "/login"
	SECURITY_SEND_REGISTER_EMAIL = False	# TODO: Weird traceback...

	# Flask-Mail
	MAIL_SERVER = "smtp.gmail.com"
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USERNAME = ""
	MAIL_PASSWORD = ""
	MAIL_DEFAULT_SENDER = ""

	# Celery
	CELERY_BROKER_URL = "redis://localhost:6379/0"
	CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
	# Celery Queues -- https://khashtamov.com/en/celery-best-practices-practical-approach/
	CELERY_QUEUES = (
		Queue('high', Exchange('high'), routing_key='high'),
		Queue('normal', Exchange('normal'), routing_key='normal'),
		Queue('low', Exchange('low'), routing_key='low'),
	)
	CELERY_DEFAULT_QUEUE = 'normal'
	CELERY_DEFAULT_EXCHANGE = 'normal'
	CELERY_DEFAULT_ROUTING_KEY = 'normal'
	# Celery SQLAlchemy Database Scheduler based of https://github.com/saadqc/celery_sqlalchemy_scheduler/tree/patch-2
	CELERYBEAT_SCHEDULER = "app.celery:DatabaseScheduler"

	# Redis
	REDIS_HOST = "localhost"
	REDIS_PORT = 6379
	REDIS_DB = "0"


class ProdConfig(Config):
	# Flask-SQLAlchemy
	SQLALCHEMY_DATABASE_URI = "postgresql://localhost/blake"


class StageConfig(Config):
	# Flask
	DEBUG = True

	# Flask-SQLAlchemy
	SQLALCHEMY_DATABASE_URI = "postgresql://localhost/blake-stage"


config = {
	"prod": ProdConfig,
	"stage": StageConfig,
	"default": StageConfig
}
