import logging
from flask_jwt_extended import create_access_token
from mysql.connector import Error

from src.DBUtils.connection.database_connection import DatabaseConnection
from src.DBUtils.auth.authdao import AuthDAO
from src.authentication.config.auth_config_loader import AuthConfig
from src.utils.exceptions.exceptions import DataBaseException, ApplicationError, InvalidUsernameOrPasswordException


logger = logging.getLogger('main.login')

LOGIN_ERROR_MESSAGE = 'There was some problem with Database.'
INVALID_USERNAME_OR_PASSWORD_MESSAGE = 'Invalid Username or password.'


class CustomerLoginHandler:
    @staticmethod
    def login_customer(email, password):
        try:
            with DatabaseConnection() as conn:

                a_dao = AuthDAO(conn)
                c_id = a_dao.login_user(email, password, AuthConfig.CUST_AUTH)
                logger.info(f"Employee with c_id:{c_id} logged in")

            return c_id

        except InvalidUsernameOrPasswordException as ie:
            logger.error(f'Invalid Username or password detected.')
            raise ApplicationError(code=401, message=INVALID_USERNAME_OR_PASSWORD_MESSAGE)
        except Error as err:
            logger.error(f'Customer login: MySQL error {err}')
            raise DataBaseException(LOGIN_ERROR_MESSAGE)

    @staticmethod
    def generate_token(cust_id):
        additional_claims = {
            'role': AuthConfig.CUSTOMER
        }
        token = create_access_token(identity=cust_id, additional_claims=additional_claims)
        return token
