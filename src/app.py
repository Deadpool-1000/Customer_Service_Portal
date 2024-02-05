import logging
import yaml
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from src.handlers.authentication.logout.BLOCKLIST import BLOCKLIST

LOG_FILE_PATH = './utils/logs/logs.log'
logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                    datefmt="%d-%m-%Y %H:%M:%S", level=logging.DEBUG, filename=LOG_FILE_PATH)
logger = logging.getLogger("main")


# Application Factory
def create_app():
    """Application factory pattern"""
    load_dotenv()
    app = Flask(__name__)

    # Load swagger, flask app and custom configurations
    app.config.from_object('config.Config')
    app.config.from_file('config_files/csm.yml', load=yaml.safe_load, text=False)
    app.config.from_file('config_files/queries.yml', load=yaml.safe_load, text=False)

    api = Api(app)
    jwt = JWTManager(app)

    # Register custom jwt error handlers
    register_jwt_error_handlers(app, jwt)

    # Register blueprints for various resource
    with app.app_context():
        from src.resources import user_blueprint
        from src.resources import ticket_blueprint
        from src.resources import feedback_blueprint
        from src.resources import message_blueprint

        register_blueprints(api, user_blueprint, ticket_blueprint, feedback_blueprint, message_blueprint)

    return app


def register_blueprints(api, *blueprints):
    for blueprint in blueprints:
        api.register_blueprint(blueprint)


def register_jwt_error_handlers(app, jwt):
    @jwt.token_in_blocklist_loader
    def check_token_in_blocklist(jwt_header, jwt_payload):
        """Called every time a JWT token is received and validates if the token has been revoked"""
        return jwt_payload['jti'] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_loader(jwt_header, jwt_payload):
        """Called every time a revoked JWT token is used"""
        return jsonify({
            'message': app.config['REVOKED_TOKEN_MESSAGE']
        }), 401
