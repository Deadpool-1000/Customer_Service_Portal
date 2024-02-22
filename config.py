import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    """App wide configuration (Swagger-UI and jwt-secret key)"""
    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Customer Service Management"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SECURITY_PARAMETERS = {
        'name': 'Authorization',
        'in': 'header',
        'description': 'Authorization: Bearer <access_token>',
        'required': 'true'
    }
