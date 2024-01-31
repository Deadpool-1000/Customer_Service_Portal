import logging
import hashlib
from flask_jwt_extended import create_access_token
from mysql.connector import Error

from src.DBUtils.connection.database_connection import DatabaseConnection
from src.DBUtils.auth.authdao import AuthDAO
from src.handlers import CSMConfig
from src.utils.exceptions.exceptions import DataBaseException, ApplicationError, InvalidUsernameOrPasswordException


logger = logging.getLogger('main.login')

LOGIN_ERROR_MESSAGE = 'There was some problem with Database.'
INVALID_USERNAME_OR_PASSWORD_MESSAGE = 'Invalid Username or password.'


class CustomerLoginHandler:
    @staticmethod
    def login_customer(email, password):
        try:
            with (DatabaseConnection() as conn):
                with AuthDAO(conn) as a_dao:
                    customer = a_dao.find_user(email, CSMConfig.CUST_AUTH)

                    # Invalid email
                    if customer is None:
                        raise ApplicationError(code=401, message=INVALID_USERNAME_OR_PASSWORD_MESSAGE)

                    # Invalid password
                    if customer['password'] != hashlib.sha256(password.encode()).hexdigest():
                        raise ApplicationError(code=401, message=INVALID_USERNAME_OR_PASSWORD_MESSAGE)

                    logger.info(f"Customer with c_id:{customer['c_id']} logged in")

            return customer['c_id']

        except Error as err:
            logger.error(f'Customer login: MySQL error {err}')
            raise DataBaseException(LOGIN_ERROR_MESSAGE)

    @staticmethod
    def generate_token(cust_id):
        additional_claims = {
            'role': CSMConfig.CUSTOMER
        }
        token = create_access_token(identity=cust_id, additional_claims=additional_claims)
        return token
