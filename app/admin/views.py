from flask import current_app, render_template, make_response, jsonify
from . import admin_bp


@admin_bp.route("/")
def admin_admin():
	return render_template("admin/admin.html")
