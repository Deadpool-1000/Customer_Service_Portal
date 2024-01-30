import logging
from mysql.connector import Error
from flask_jwt_extended import create_access_token

from src.handlers import CSMConfig
from src.DBUtils.connection.database_connection import DatabaseConnection
from src.DBUtils.employee.employeedao import EmployeeDAO
from src.DBUtils.auth.authdao import AuthDAO
from src.utils.exceptions.exceptions import DataBaseException


logger = logging.getLogger('main.employee_login_handler')
LOGIN_ERROR_MESSAGE = 'There was some problem while logging you in.'


class EmployeeLoginHandler:
    @staticmethod
    def login_employee(email, password):
        try:
            with DatabaseConnection() as conn:
                with AuthDAO(conn) as a_dao:
                    emp_details = a_dao.login_user(email, password, CSMConfig.EMP_AUTH)

                logger.info(f"Employee with e_id:{emp_details['e_id']}, role:{emp_details['designation']} logged in")

            return {
                'e_id': emp_details['e_id'],
                'role': emp_details['designation']
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
