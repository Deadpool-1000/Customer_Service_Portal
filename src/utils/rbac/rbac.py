from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask_smorest import abort
from functools import wraps
from src.handlers import CSMConfig


CUSTOMER = 'CUSTOMER'
HELPDESK = 'HELPDESK'
MANAGER = 'MANAGER'


def access_required(roles_allowed):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            allowed = []
            for role in roles_allowed:
                if role == CUSTOMER:
                    allowed.append(CSMConfig.CUSTOMER)
                elif role == HELPDESK:
                    allowed.append(CSMConfig.HELPDESK)
                elif role == MANAGER:
                    allowed.append(CSMConfig.MANAGER)

            token = get_jwt()
            if token['role'] in allowed:
                return func(*args, **kwargs)
            else:
                abort(403, message='You dont have enough permission to access this.')
        return wrapper

    return decorator
