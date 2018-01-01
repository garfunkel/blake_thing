from flask import Blueprint
from flask_security import login_required


main_bp = Blueprint("main", __name__)


@main_bp.before_request
@login_required
def before_request():
	pass


from . import views
