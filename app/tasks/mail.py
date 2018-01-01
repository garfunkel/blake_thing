from flask import current_app, render_template
from flask_mail import Message

from app import mail, celery


@celery.task
def send_async_email(msg):
	mail.send(msg)

def send_mail(to, subject, template, **kwargs):
	msg = Message(subject, recipients=to)
	msg.body = render_template(template + ".txt", **kwargs)
	msg.html = render_template(template + ".html", **kwargs)
	send_async_email.delay(msg)
