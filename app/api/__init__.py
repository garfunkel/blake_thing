from flask import Blueprint
from flask_restful import Api


api_bp = Blueprint("api", __name__)
api = Api(api_bp)


from . import shares
api.add_resource(shares.Shares_API, "/shares", endpoint="shares")
api.add_resource(shares.Share_API, "/shares/<int:id>", endpoint="share")

from . import stores
api.add_resource(stores.Stores_API, "/stores", endpoint="stores")
api.add_resource(stores.Store_API, "/stores/<int:id>", endpoint="store")

from . import scripts
api.add_resource(scripts.Scripts_API, "/scripts", endpoint="scripts")
api.add_resource(scripts.Script_API, "/scripts/<string:name>", endpoint="script")

from . import jobs
api.add_resource(jobs.Jobs_API, "/jobs", endpoint="jobs")
api.add_resource(jobs.Job_API, "/jobs/<int:id>", endpoint="job")
