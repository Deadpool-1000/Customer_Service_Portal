from flask_smorest import abort
from src.handlers.authentication.employee.employee_login_handler import EmployeeLoginHandler
from src.utils.exceptions import ApplicationError, DataBaseException
from src.handlers import CSMConfig


class EmployeeLoginController:
    @staticmethod
    def login(emp_data):
        email = emp_data['email']
        password = emp_data['password']
        try:
            employee_auth_details = EmployeeLoginHandler.login_employee(email, password)
            token = EmployeeLoginHandler.generate_token(employee_auth_details)

            return {
                'token': token
            }

        except ApplicationError as ae:
            abort(ae.code, message=ae.message)

        except DataBaseException:
            abort(500, message=CSMConfig.LOGIN_ERROR_MESSAGE)
