from flask import current_app, render_template, make_response, jsonify
from . import main_bp


@main_bp.route("/")
def main_blake():
	return render_template("blake.html")


@main_bp.route("/scripts")
def main_scripts():
	return render_template("scripts.html")


@main_bp.route("/jobs")
def main_jobs():
	return render_template("jobs.html")


@main_bp.route("/syncs")
def main_syncs():
	return render_template("syncs.html")


@main_bp.route("/account")
def account():
	return render_template("account.html")
