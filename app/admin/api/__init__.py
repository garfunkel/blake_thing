from flask_restful import Api
from .. import admin_bp


api = Api(admin_bp, "/api")
