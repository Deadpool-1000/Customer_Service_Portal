from functools import wraps
from flask import current_app
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask_smorest import abort


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
            token = get_jwt()
            if token['role'] in roles_allowed:
                return func(*args, **kwargs)
            else:
                abort(403, message=current_app.config['UNAUTHORIZED_ERROR_MESSAGE'])

        return wrapper

    return decorator
