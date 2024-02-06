from functools import wraps

from flask import current_app
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask_smorest import abort

CUSTOMER = 'CUSTOMER'
HELPDESK = 'HELPDESK'
MANAGER = 'MANAGER'


def access_required(roles_allowed):
    """Roles based access control"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            This function checks jwt in request and further verifies if the role in token is in the roles_allowed iterable.
            If the role inside jwt payload is in roles_allowed then the decorated function is allowed to run. Otherwise a 403 exception is sent to user.
            """
            verify_jwt_in_request()
            allowed = []
            for role in roles_allowed:
                if role == CUSTOMER:
                    allowed.append(current_app.config['CUSTOMER'])
                elif role == HELPDESK:
                    allowed.append(current_app.config['HELPDESK'])
                elif role == MANAGER:
                    allowed.append(current_app.config['MANAGER'])

            token = get_jwt()
            if token['role'] in allowed:
                return func(*args, **kwargs)
            else:
                abort(403, message=current_app.config['UNAUTHORIZED_ERROR_MESSAGE'])

        return wrapper

    return decorator
