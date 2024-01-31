import logging
import hashlib
from mysql.connector import Error
from flask_jwt_extended import create_access_token

from src.handlers import CSMConfig
from src.DBUtils.connection.database_connection import DatabaseConnection
from src.DBUtils.employee.employeedao import EmployeeDAO
from src.DBUtils.auth.authdao import AuthDAO
from src.utils.exceptions.exceptions import DataBaseException, ApplicationError


logger = logging.getLogger('main.employee_login_handler')
LOGIN_ERROR_MESSAGE = 'There was some problem while logging you in.'
INVALID_USERNAME_OR_PASSWORD_MESSAGE = 'Invalid Username or password.'


class EmployeeLoginHandler:
    @staticmethod
    def login_employee(email, password):
        try:
            with DatabaseConnection() as conn:
                with AuthDAO(conn) as a_dao:
                    employee = a_dao.find_user(email, CSMConfig.EMP_AUTH)

                    if employee is None:
                        raise ApplicationError(code=401, message=INVALID_USERNAME_OR_PASSWORD_MESSAGE)

                    if employee['password'] != hashlib.sha256(password.encode()).hexdigest():
                        raise ApplicationError(code=401, message=INVALID_USERNAME_OR_PASSWORD_MESSAGE)

                logger.info(f"Employee with e_id:{employee['e_id']}, role:{employee['designation']} logged in")

            return {
                'e_id': employee['e_id'],
                'role': employee['designation']
            }

        except Error as err:
            logger.error(f'Employee login: {err}')
            raise DataBaseException(LOGIN_ERROR_MESSAGE)

    @staticmethod
    def generate_token(employee_auth_details):
        e_id = employee_auth_details['e_id']
        role = employee_auth_details['role']

        additional_claims = {
            'role': CSMConfig.MANAGER if role == 'manager' else CSMConfig.HELPDESK
        }

        token = create_access_token(identity=e_id, additional_claims=additional_claims)
        return token
