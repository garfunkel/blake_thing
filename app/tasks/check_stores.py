import os
import datetime

from flask import current_app

from app import celery, db
from app.models import Store


@celery.task
def check_stores():
	print("Running")
	app = current_app._get_current_object()
	current_date = datetime.datetime.now() + datetime.timedelta(days=app.config["BLAKE_MAX_STORE_DAYS"])

	stores = []
	for store in Store.query.all():
		print(store)
		last_modif = store.modified.timestamp()
		for dirpath, _, filenames in os.walk(store.full_path):
			for filename in filenames:
				modif_date = os.stat(os.path.join(dirpath, filename)).st_mtime
				if modif_date > last_modif:
					last_modif = modif_date
		if last_modif == store.modified.timestamp():
			stores.append(store.path)
		else:
			store.modified = datetime.datetime.fromtimestamp(last_modif)
			db.session.commit()
