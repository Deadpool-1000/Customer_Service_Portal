from flask import current_app
from flask_smorest import abort

from src.controllers.authentication.login import CustomerLoginController, EmployeeLoginController


class LoginController:
    @staticmethod
    def login(login_data):
        role = login_data['role']

        if role == current_app.config['CUSTOMER_']:
            return CustomerLoginController.login(login_data)
        elif role == current_app.config['EMPLOYEE_']:
            return EmployeeLoginController.login(login_data)
        else:
            abort(400, message=current_app.config['INVALID_ROLE_ERROR_MESSAGE'])
