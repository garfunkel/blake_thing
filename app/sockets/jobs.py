import json
from threading import Lock

from flask import current_app
from flask_socketio import Namespace, emit

from app import socketio, redis

thread =None
thread_lock = Lock()


# TODO: re-write this... temp for testing...
def background_thread(app):
	with app.app_context():
		count = 0
		while True:
			socketio.sleep(3)
			jobs = []

			for key in redis.keys():
				if key.startswith(b"celery-task-meta"):
					key = json.loads(redis.get(key))
					if key["status"] == "PROGRESS":
						jobs.append(key)

			socketio.emit("ASD",
							{"data": jobs},
							namespace="/jobs")

class JobsNamespace(Namespace):
	def on_connect(self):
		global thread
		with thread_lock:
			if thread == None:
				thread = socketio.start_background_task(background_thread, current_app._get_current_object())
		emit("my_response", {"data": 0})

	def on_disconnect(self):
		pass
