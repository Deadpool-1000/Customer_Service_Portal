from flask import current_app
from flask.views import MethodView
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from flask_smorest import Blueprint

from src.controllers.authentication.login.login_controller import LoginController
from src.controllers.authentication.logout.logout_controller import LogoutController
from src.controllers.authentication.signup.customer_signup_controller import CustomerSignupController
from src.controllers.user.user_controller import UserController
from src.schemas.error import CustomErrorSchema
from src.schemas.user import UserSignupSchema, AuthSchemaRole, SuccessSchema, TokenSchema, ProfileSchema
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

PROFILE_EXAMPLE = {
    "address": "Abc-street, XYZ city",
    "c_id": "qo3Mh",
    "email": "Myron32@gmail.com",
    "full_name": "Maximilian95",
    "phn_num": "4678932824",
    "role": "CUSTOMER"
}

PROFILE_UPDATE_EXAMPLE = {
    "message": "Profile Updated Successfully."
}


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


@blp.route('/profile')
class Profile(MethodView):
    @blp.alt_response(HTTP_401_UNAUTHORIZED, schema=CustomErrorSchema, example=UNAUTHORIZED_EXAMPLE, description=NO_JWT_PROVIDED_DESCRIPTION)
    @blp.response(HTTP_200_OK, schema=ProfileSchema, example=PROFILE_EXAMPLE)
    @jwt_required()
    def get(self):
        """Get profile"""
        role = get_jwt()['role']
        user_id = get_jwt_identity()
        return UserController.get_profile(user_id=user_id, role=role)

    @blp.alt_response(HTTP_401_UNAUTHORIZED, schema=CustomErrorSchema, example=UNAUTHORIZED_EXAMPLE, description=NO_JWT_PROVIDED_DESCRIPTION)
    @blp.response(HTTP_200_OK, schema=SuccessSchema, example=PROFILE_UPDATE_EXAMPLE)
    @blp.arguments(ProfileSchema)
    @access_required([current_app.config['CUSTOMER']])
    def put(self, new_user_data):
        """Update profile for customer"""
        user_id = get_jwt_identity()
        return UserController.put_customer_profile(user_id, new_user_data)

