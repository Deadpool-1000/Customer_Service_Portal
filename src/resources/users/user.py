from flask import current_app, request
from flask.views import MethodView
from flask_jwt_extended import get_jwt, jwt_required
from flask_smorest import Blueprint

from src.controllers.authentication.customer.customer_login_controller import CustomerLoginController
from src.controllers.authentication.customer.customer_signup_controller import CustomerSignupController
from src.controllers.authentication.employee.employee_login_controller import EmployeeLoginController
from src.controllers.authentication.logout.logout_controller import LogoutController
from src.schemas.user import UserSignupSchema, AuthSchema, TokenSchema, SuccessSchema

blp = Blueprint('Users', 'users', description='Operation on users')


@blp.route('/login/customer')
class LoginCustomer(MethodView):
    @blp.arguments(AuthSchema)
    @blp.response(200, TokenSchema)
    def post(self, cust_auth_data):
        current_app.logger.debug("POST /login/customer")
        token = CustomerLoginController.login(cust_auth_data)
        return token


@blp.route('/login/employee')
class LoginEmployee(MethodView):
    @blp.response(200, TokenSchema)
    @blp.arguments(AuthSchema)
    def post(self, emp_data):
        current_app.logger.debug("POST /login/employee")
        print("request id", request.request_id)
        print(request.environ['X-Request-Id'])
        token = EmployeeLoginController.login(emp_data)
        return token


@blp.route('/signup')
class SignupCustomer(MethodView):
    @blp.response(201, SuccessSchema)
    @blp.arguments(UserSignupSchema)
    def post(self, cust_data):
        current_app.logger.debug("POST /signup")
        print("Request headers", request.request_id)
        success_message = CustomerSignupController.signup(cust_data)
        return success_message


@blp.route('/logout')
class Logout(MethodView):
    @jwt_required()
    def post(self):
        current_app.logger.debug("POST /logout")
        token = get_jwt()
        success_message = LogoutController.logout(token)
        return success_message, 200
