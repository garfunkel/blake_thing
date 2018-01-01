from flask import Blueprint
from flask_security import login_required, roles_required


admin_bp = Blueprint("admin", __name__, template_folder="templates", static_folder="static")


@admin_bp.before_request
@login_required
@roles_required('admin')
def before_request():
	pass


from . import views
from . import api
