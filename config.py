import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Customer Service Management"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_RAPIDOC_PATH = "/rapidoc"
    OPENAPI_RAPIDOC_URL = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
