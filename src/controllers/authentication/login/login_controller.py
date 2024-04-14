from flask import current_app
from flask_smorest import abort

from src.controllers.authentication.login import CustomerLoginController, EmployeeLoginController


class LoginController:
    @staticmethod
    def login(login_data):
        role = login_data['role']
        token = {}
        if role == current_app.config['CUSTOMER_']:
            token = CustomerLoginController.login(login_data)
        elif role == current_app.config['EMPLOYEE_']:
            token = EmployeeLoginController.login(login_data)
        else:
            abort(400, message=current_app.config['INVALID_ROLE_ERROR_MESSAGE'])
        return {
            'token': token,
            'expiresIn': current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()
        }
