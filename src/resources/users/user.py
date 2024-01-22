from flask.views import MethodView
from flask_smorest import Blueprint


blp = Blueprint('Users', 'users', description='Operation on users')


@blp.route('/login/customer')
class LoginCustomer(MethodView):
    def post(self):
        pass


@blp.route('/login/employee')
class LoginEmployee(MethodView):
    def post(self):
        pass


@blp.route('/signup')
class SignupCustomer(MethodView):
    def post(self):
        pass


@blp.route('/logout')
class Logout(MethodView):
    def post(self):
        pass
