from flask.views import MethodView
from flask_smorest import Blueprint

from src.schemas.user import UserSignupSchema, AuthSchema, TokenSchema, SuccessSchema

from src.controllers.authentication.customer.customer_login_controller import CustomerLoginController
from src.controllers.authentication.employee.employee_login_controller import EmployeeLoginController
from src.controllers.authentication.customer.customer_signup_controller import CustomerSignupController


blp = Blueprint('Users', 'users', description='Operation on users')


@blp.route('/login/customer')
class LoginCustomer(MethodView):
    @blp.arguments(AuthSchema)
    @blp.response(200, TokenSchema)
    def post(self, cust_auth_data):
        token = CustomerLoginController.login(cust_auth_data)
        return token


@blp.route('/login/employee')
class LoginEmployee(MethodView):

    @blp.response(200, TokenSchema)
    @blp.arguments(AuthSchema)
    def post(self, emp_data):
        token = EmployeeLoginController.login(emp_data)
        return token


@blp.route('/signup')
class SignupCustomer(MethodView):
    @blp.response(201, SuccessSchema)
    @blp.arguments(UserSignupSchema)
    def post(self, cust_data):
        success_message = CustomerSignupController.signup(cust_data)
        return success_message


@blp.route('/logout')
class Logout(MethodView):
    def post(self):
        pass
