import os

from flask_migrate import Migrate

from app import create_app, db
from app.models import *

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


@app.cli.command()
def cleardb():
	"""Clears database tables."""
	meta = db.metadata
	for table in reversed(meta.sorted_tables):
		print("Clearing {}".format(table))
		db.session.execute(table.delete())
	db.session.commit()


@app.cli.command()
def init():
	# Add default audio_store checking script
	check_stores = DatabaseSchedulerEntry()
	check_stores.name = "check_stores"
	check_stores.task = "app.tasks.check_stores.check_stores"
	check_stores.celery_crontabs = CrontabSchedule()
	check_stores.celery_crontabs.minute = '*/5' # Every 5 min

	db.session.add(check_stores)
	db.session.commit()


@app.cli.command()
def fill():
	# Create test audiostore directory
	audio_store_directory = os.path.join(os.getcwd(), "test_store")
	os.mkdir(audio_store_directory)

	audio_store = Share(audio_store_directory)

	db.session.add(audio_store)
	db.session.commit()
