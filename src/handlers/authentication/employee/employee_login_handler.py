import hashlib
from flask import current_app
from flask_jwt_extended import create_access_token
import pymysql

from src.dbutils.auth.auth_dao import AuthDAO
from src.dbutils.connection.database_connection import DatabaseConnection
from src.utils.exceptions.exceptions import DataBaseException, ApplicationError


class EmployeeLoginHandler:
    @staticmethod
    def login_employee(email, password):
        """Verify employee email and password and returns employee auth data that contains role and employee identification number"""
        try:
            with DatabaseConnection() as conn:
                with AuthDAO(conn) as a_dao:
                    employee = a_dao.find_user(email, current_app.config['EMP_AUTH'])

                    if employee is None:
                        current_app.logger.error(f"Employee Login: Invalid email {email} provided.")
                        raise ApplicationError(code=401,
                                               message=current_app.config['INVALID_USERNAME_OR_PASSWORD_MESSAGE'])

                    if employee['password'] != hashlib.sha256(password.encode()).hexdigest():
                        current_app.logger.error(f"Employee with email {email} provided wrong password.")
                        raise ApplicationError(code=401,
                                               message=current_app.config['INVALID_USERNAME_OR_PASSWORD_MESSAGE'])

                current_app.logger.info(
                    f"Employee with e_id:{employee['e_id']}, role:{employee['designation']} logged in")

            return {
                'e_id': employee['e_id'],
                'role': employee['designation']
            }

        except pymysql.Error as e:
            current_app.logger.error(f'Employee login: {e.args[0]}: {e.args[1]}')
            raise DataBaseException(current_app.config['LOGIN_ERROR_MESSAGE']) from e

    @staticmethod
    def generate_token(employee_auth_details):
        """Generates access token based on employee identification number and role"""
        e_id = employee_auth_details['e_id']
        role = employee_auth_details['role']

        additional_claims = {
            'role': current_app.config['MANAGER'] if role == 'manager' else current_app.config['HELPDESK']
        }

        token = create_access_token(identity=e_id, additional_claims=additional_claims)
        return token
