import os

from app import celery, create_app
import app.tasks

app = create_app(os.getenv("FLASK_CONFIG") or "default")
app.app_context().push()
