from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask_smorest import abort
from functools import wraps
from src.authentication.config.auth_config_loader import AuthConfig


def access_required(roles_allowed):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            allowed = []
            for role in roles_allowed:
                if role == 'CUSTOMER':
                    allowed.append(AuthConfig.CUSTOMER)
                elif role == 'HELPDESK':
                    allowed.append(AuthConfig.HELPDESK)
                elif role == 'MANAGER':
                    allowed.append(AuthConfig.MANAGER)

            verify_jwt_in_request()
            token = get_jwt()
            print(token['role'])
            print(roles_allowed)
            if token['role'] in allowed:
                return func(*args, **kwargs)
            else:
                abort(403, message='You dont have enough permission to access this.')
        return wrapper

    return decorator
