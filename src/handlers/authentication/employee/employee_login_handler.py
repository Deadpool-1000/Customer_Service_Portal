import logging
from mysql.connector import Error
from flask_jwt_extended import create_access_token

from src.authentication.config.auth_config_loader import AuthConfig
from src.DBUtils.connection.database_connection import DatabaseConnection
from src.DBUtils.employee.employeedao import EmployeeDAO
from src.DBUtils.auth.authdao import AuthDAO
from src.utils.exceptions.exceptions import DataBaseException


logger = logging.getLogger('main.employee_login_handler')


class EmployeeLoginHandler:
    @staticmethod
    def login_employee(email, password):
        try:
            with DatabaseConnection() as conn:
                with AuthDAO(conn) as a_dao:
                    emp_details = a_dao.login_user(email, password, AuthConfig.EMP_AUTH)

                logger.info(f"Employee with e_id:{emp_details['e_id']}, role:{emp_details['designation']} logged in")

            return {
                'e_id': emp_details['e_id'],
                'role': emp_details['designation']
            }

        except Error as err:
            logger.error(f'Employee login: {err}')
            raise DataBaseException('There was some problem while logging you in.')

    @staticmethod
    def generate_token(employee_auth_details):
        e_id = employee_auth_details['e_id']
        role = employee_auth_details['role']

        print("generate token ", e_id, role)

        additional_claims = {
            'role': AuthConfig.MANAGER if role == 'manager' else AuthConfig.CUSTOMER
        }

        token = create_access_token(identity=e_id, additional_claims=additional_claims)
        return token
