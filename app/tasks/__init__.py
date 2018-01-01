import os

from .check_stores import check_stores

from app import celery, db
from app.scripts import scripts, load_scripts
from app.models import Job

# For testing... TODO: Redo & relocate to better place...
@celery.task(bind=True)
def runScript(self, name, data):
	load_scripts()

	# Very much tempo.. ya know
	job = Job()
	job.task_id = self.request.id
	db.session.add(job)
	db.session.commit()

	os.mkdir(job.path)
	os.chdir(job.path)

	script = scripts[name].parse(data, self)
	script.run()
