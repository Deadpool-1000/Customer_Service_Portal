import yaml
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_smorest import Api

from src.handlers.authentication.logout.BLOCKLIST import BLOCKLIST
from src.utils.utils import RequestFormatter, generate_new_request_id


# Application Factory
def create_app():
    """Application factory pattern"""
    load_dotenv()
    app = Flask(__name__)

    configure_logging(app)

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
        register_before_request_handler(app)

    @app.route("/status", methods=["GET"])
    def status():
        return {
            "status": "Happy 🙂"
        }, 200

    return app


def register_blueprints(api, *blueprints):
    """Register blueprints for every resource"""
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
        app.logger.error(f"Identity {jwt_payload['sub']} tried to use a revoked token.")
        return jsonify({
            'code': 401,
            'status': 'Unauthorized',
            'message': app.config['REVOKED_TOKEN_MESSAGE']
        }), 401

    @jwt.unauthorized_loader
    def no_jwt_token_loader(reason):
        print(reason)
        return jsonify({
            'code': 401,
            'status': 'Unauthorized',
            'message': app.config['NO_JWT_TOKEN_MESSAGE']
        }), 401


def configure_logging(app):
    """Logging configurations"""
    import logging
    from flask.logging import default_handler
    from logging.handlers import SysLogHandler

    # Deactivate the default flask logger so that log messages don't get duplicated
    app.logger.removeHandler(default_handler)

    # Create a file handler object
    papertrail_log = SysLogHandler(address=('logs3.papertrailapp.com', 14400))

    # Set the logging level of the file handler object so that it logs INFO and up
    papertrail_log.setLevel(logging.DEBUG)

    # Create a file formatter object
    file_formatter = RequestFormatter('%(asctime)s %(levelname)s %(request_id)s : %(message)s [in %(filename)s: %(lineno)d]')

    # Apply the file formatter object to the file handler object
    papertrail_log.setFormatter(file_formatter)

    # Add file handler object to the logger
    app.logger.addHandler(papertrail_log)


def register_before_request_handler(app):
    @app.before_request
    def add_request_id():
        """Adds request id to the request object for logging"""
        request_id = generate_new_request_id()
        request.request_id = request_id
