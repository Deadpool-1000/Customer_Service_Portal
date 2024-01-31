import os
import logging
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from src.utils.load_configurations import load_configurations
from src.resources import user_blueprint
from src.resources import ticket_blueprint
from src.resources import feedback_blueprint
from src.resources import message_blueprint
from src.handlers.authentication.logout.BLOCKLIST import BLOCKLIST

LOG_FILE_PATH = 'utils/logs/logs.log'


logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                    datefmt="%d-%m-%Y %H:%M:%S", level=logging.DEBUG, filename=LOG_FILE_PATH)
logger = logging.getLogger("main")


def create_app():
    # docstring
    # nested response
    load_dotenv()
    app = Flask(__name__)
    # change the location of below
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Customer Service Management"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_JSON_PATH"] = "api-spec.json"
    app.config["OPENAPI_REDOC_PATH"] = "/redoc"
    app.config["OPENAPI_REDOC_URL"] = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["OPENAPI_RAPIDOC_PATH"] = "/rapidoc"
    app.config["OPENAPI_RAPIDOC_URL"] = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"
    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')

    with app.app_context():
        load_configurations()

    api = Api(app)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_loader(jwt_header, jwt_payload):
        return jsonify({
            'message': 'Your token is revoked, Please log in to continue.'
        }), 401

    api.register_blueprint(user_blueprint)
    api.register_blueprint(ticket_blueprint)
    api.register_blueprint(feedback_blueprint)
    api.register_blueprint(message_blueprint)

    return app
