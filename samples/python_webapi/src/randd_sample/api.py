import logging
from flask import Blueprint, Flask, jsonify, request
from .schema.validator import validate_sample_request
from .service import RegressionService


bp = Blueprint('api', __name__, url_prefix="/v1")


@bp.route("/sample")
def route_sample():
    return "Sample."


@bp.route("/analyse", methods=["POST"])
def analyse():
    validate_sample_request(request.get_json())
    result = RegressionService.predict(request.get_json())
    return jsonify({"MEDV": result})


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    @app.route("/")
    def health_check():
        app.logger.info("Health check.")
        return "I'm fine. Thank you, and you ?"

    return app


app = create_app()
