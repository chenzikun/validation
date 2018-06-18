import pytest
from flask import Blueprint, Flask
from flask.json import jsonify

from validations.managers import request_validation


class Application(Flask):
    def __init__(self, environment):
        super(Application, self).__init__(__name__)
        if environment == "dev":
            self.config.Debug = True
        self.register_bps()

    def register_bps(self):
        for bp in [param_bp]:
            self.register_blueprint(bp)


param_bp = Blueprint("param", __name__, )


@param_bp.route("/", methods=["GET", "POST"])
def index():
    return "hello"


@param_bp.route("/auth", methods=["GET", "POST"])
@request_validation(server_type="auth")
def auth():
    re = {"code": 0, "message": "auth"}
    return jsonify(re)


@param_bp.route("/domain", methods=["GET", "POST"])
@request_validation(server_type="domain")
def domain():
    return jsonify()


@param_bp.route("/url", methods=["GET", "POST"])
@request_validation(server_type="url")
def url():
    return jsonify()


@param_bp.route("/ips", methods=["GET", "POST"])
@request_validation(server_type="ips")
def ips():
    return jsonify()


@param_bp.route("/file_hash", methods=["GET", "POST"])
@request_validation(server_type="file_hash")
def file_hash():
    return jsonify()


@param_bp.route("/file_scan", methods=["GET", "POST"])
@request_validation(server_type="file_scan")
def file_scan():
    return jsonify()


@param_bp.route("/safe_events", methods=["GET", "POST"])
@request_validation(server_type="safe_events")
def safe_events():
    return jsonify()


@param_bp.route("/threats_intelligence", methods=["GET", "POST"])
@request_validation(server_type="threats_intelligence")
def threats_intelligence():
    return jsonify()


@param_bp.route("/collect_files", methods=["GET", "POST"])
@request_validation(server_type="collect_files")
def collect_files():
    return jsonify()


@param_bp.route("/collect_logs", methods=["GET", "POST"])
@request_validation(server_type="collect_logs")
def collect_logs():
    return jsonify()


@param_bp.route("/file_issued", methods=["GET", "POST"])
@request_validation(server_type="file_issued")
def file_issued():
    return jsonify()


@pytest.fixture
def app():
    app = Application("test")
    return app
