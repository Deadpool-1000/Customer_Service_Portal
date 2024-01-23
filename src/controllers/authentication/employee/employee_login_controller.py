from flask_smorest import abort
from src.handlers.authentication.employee.employee_login_handler import EmployeeLoginHandler
from src.schemas.user import TokenSchema
from src.utils.exceptions import InvalidUsernameOrPasswordException, DataBaseException


class EmployeeLoginController:
    @staticmethod
    def login(emp_data):
        email = emp_data['email']
        password = emp_data['password']

        try:
            employee_auth_details = EmployeeLoginHandler.login_employee(email, password)
            token = EmployeeLoginHandler.generate_token(employee_auth_details)
            return TokenSchema().load({
                'token': token
            })

        except InvalidUsernameOrPasswordException:
            abort(401, message='Invalid Username or password provided.')

        except DataBaseException:
            abort(500, message="There was some problem while logging you in.")
