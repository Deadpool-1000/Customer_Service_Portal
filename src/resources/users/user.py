from flask import current_app
from flask.views import MethodView
from flask_jwt_extended import get_jwt
from flask_smorest import Blueprint

from src.controllers.authentication.login.login_controller import LoginController
from src.controllers.authentication.logout.logout_controller import LogoutController
from src.schemas.error import CustomErrorSchema
from src.schemas.user import UserSignupSchema, AuthSchemaRole, SuccessSchema, TokenSchema
from src.utils.rbac.rbac import access_required

blp = Blueprint('Users', 'users', description='Operation on users')

HTTP_201_CREATED = 201
HTTP_409_CONFLICT = 409
HTTP_200_OK = 200
HTTP_401_UNAUTHORIZED = 401
NO_JWT_PROVIDED_DESCRIPTION = "No valid JWT token provided in the Authorization header."
INCORRECT_CREDENTIALS_DESCRIPTION = "Incorrect credentials provided in the request."
CONFLICT_MESSAGE_DESCRIPTION = "Email already in use."


SIGNUP_CONFLICT_EXAMPLE = {
    'code': HTTP_409_CONFLICT,
    'status': 'Conflict',
    'message': 'Email taken.'
}

LOGIN_UNAUTHORIZED_EXAMPLE = {
    'code': HTTP_401_UNAUTHORIZED,
    'status': 'Unauthorized',
    'message': 'Incorrect email or password provided.'
}

UNAUTHORIZED_EXAMPLE = {
    'code': HTTP_401_UNAUTHORIZED,
    'status': 'Unauthorized',
    'message': 'Please provide a valid JWT token in the Authorization header.'
}

TOKEN_EXAMPLE = {
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
             '.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNzM3Mzk2NiwianRpIjoiZjRhNjMwN2UtMmExMi00NWI0LWI3Y2QtZGIwZTc1ZjExMmExIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IkxMWVdpIiwibmJmIjoxNzA3MzczOTY2LCJjc3JmIjoiMTFlZDk1YmQtYTZiYy00MjU1LTkyN2EtYjY1YzBmYTAzYTVhIiwiZXhwIjoxNzA3Mzc0ODY2LCJyb2xlIjoic3VwZXJtYW4ifQ.'
             'Ou8L1d4zL-xB6QvHmt1OkTtLzW1Y3-TF1gnR36_RDso'
}


LOGOUT_SUCCESS_EXAMPLE = {
    'message': 'Successfully Logged out.'
}

SIGNUP_SUCCESS_EXAMPLE = {
    'message': 'Signup Successful.'
}

"""
@blp.route('/login/customer')
class LoginCustomer(MethodView):
    @blp.alt_response(HTTP_401_UNAUTHORIZED, schema=CustomErrorSchema, example=LOGIN_UNAUTHORIZED_EXAMPLE, description=INCORRECT_CREDENTIALS_DESCRIPTION)
    @blp.response(HTTP_200_OK, TokenSchema, example=TOKEN_EXAMPLE)
    @blp.arguments(AuthSchema)
    def post(self, cust_auth_data):
        """"""Login as customer""""""
        current_app.logger.debug("POST /login/customer")
        token = CustomerLoginController.login(cust_auth_data)
        return token


@blp.route('/login/employee')
class LoginEmployee(MethodView):
    @blp.alt_response(HTTP_401_UNAUTHORIZED, schema=CustomErrorSchema, example=LOGIN_UNAUTHORIZED_EXAMPLE, description=INCORRECT_CREDENTIALS_DESCRIPTION)
    @blp.response(HTTP_200_OK, TokenSchema, example=TOKEN_EXAMPLE)
    @blp.arguments(AuthSchema)
    def post(self, emp_data):
        """"""Login as employee""""""
        current_app.logger.debug("POST /login/employee")
        token = EmployeeLoginController.login(emp_data)
        return token
"""


@blp.route('/login')
class Login(MethodView):
    @blp.alt_response(HTTP_401_UNAUTHORIZED, schema=CustomErrorSchema, example=LOGIN_UNAUTHORIZED_EXAMPLE, description=INCORRECT_CREDENTIALS_DESCRIPTION)
    @blp.response(HTTP_200_OK, TokenSchema, example=TOKEN_EXAMPLE)
    @blp.arguments(AuthSchemaRole)
    def post(self, login_data):
        token = LoginController.login(login_data)
        return token


@blp.route('/signup')
class SignupCustomer(MethodView):
    @blp.alt_response(HTTP_409_CONFLICT, schema=CustomErrorSchema, example=SIGNUP_CONFLICT_EXAMPLE, description=CONFLICT_MESSAGE_DESCRIPTION)
    @blp.response(HTTP_201_CREATED, schema=SuccessSchema, example=SIGNUP_SUCCESS_EXAMPLE)
    @blp.arguments(UserSignupSchema)
    def post(self, cust_data):
        """Signup as customer"""
        current_app.logger.debug("POST /signup")
        success_message = CustomerSignupController.signup(cust_data)
        return success_message


@blp.route('/logout')
class Logout(MethodView):
    @blp.response(HTTP_401_UNAUTHORIZED, schema=CustomErrorSchema, example=UNAUTHORIZED_EXAMPLE, description=NO_JWT_PROVIDED_DESCRIPTION)
    @blp.response(HTTP_200_OK, schema=SuccessSchema, example=LOGOUT_SUCCESS_EXAMPLE)
    @blp.doc(parameters=[current_app.config['SECURITY_PARAMETERS']])
    @access_required([current_app.config['CUSTOMER'], current_app.config['MANAGER'], current_app.config['HELPDESK']])
    def post(self):
        """Logout of the application"""
        current_app.logger.debug("POST /logout")
        token = get_jwt()
        success_message = LogoutController.logout(token)
        return success_message, 200
