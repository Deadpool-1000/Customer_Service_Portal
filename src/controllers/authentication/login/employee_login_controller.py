from flask import current_app
from flask_smorest import abort

from src.handlers.authentication.employee.employee_login_handler import EmployeeLoginHandler
from src.utils.exceptions import ApplicationError, DataBaseException

logger = current_app.logger


class EmployeeLoginController:
    @staticmethod
    def login(emp_data):
        email = emp_data['email']
        password = emp_data['password']
        try:
            employee_auth_details = EmployeeLoginHandler.login_employee(email, password)
            token = EmployeeLoginHandler.generate_token(employee_auth_details)
            logger.info(f"Employee with email {email} logged in.")
            return {
                'token': token
            }

        except ApplicationError as ae:
            abort(ae.code, message=ae.message)

        except DataBaseException as db:
            abort(500, message=str(db))
