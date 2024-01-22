import os
import logging
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from src.utils.load_configurations import load_configurations
from src.resources.users.user import blp as UserBlueprint
from src.resources.ticket.ticket import blp as TicketBlueprint
from src.resources.feedback.feedback import blp as FeedbackBlueprint
from src.resources.message.message import blp as MessageBlueprint

LOG_FILE_PATH = path.join(path_current_directory, 'utils/logs/logs.log')


logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG, filename=LOG_FILE_PATH)
logger = logging.getLogger("main")


def create_app():
    load_dotenv()
    app = Flask(__name__)

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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////DBUtils/data/csm.db'

    with app.app_context():
        load_configurations()

    api = Api(app)
    jwt = JWTManager(app)

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(TicketBlueprint)
    api.register_blueprint(FeedbackBlueprint)
    api.register_blueprint(MessageBlueprint)

    return app
