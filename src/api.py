from flask import Blueprint

bp = Blueprint("api", __name__)

@bp.route("/endpoint", methods=["GET"])
def get_endpoint():
    return '1 + 1 = 2'