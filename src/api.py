from flask import Blueprint, current_app

bp = Blueprint("api", __name__)

@bp.route("/endpoint", methods=["GET"])
def get_endpoint():
    logtail_handler = current_app.logger.handlers[0]

    current_app.logger.info("Logtail handler info %s", logtail_handler.__dict__)
    
    return '1 + 1 = 2'