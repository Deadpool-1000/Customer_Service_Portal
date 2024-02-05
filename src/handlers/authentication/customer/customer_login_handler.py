import logging
import hashlib
from flask import current_app
from flask_jwt_extended import create_access_token
from mysql.connector import Error

from src.dbutils.connection.database_connection import DatabaseConnection
from src.dbutils.auth.authdao import AuthDAO
from src.utils.exceptions.exceptions import DataBaseException, ApplicationError


logger = logging.getLogger('main.login')


class CustomerLoginHandler:
    @staticmethod
    def login_customer(email, password):
        try:
            with (DatabaseConnection() as conn):
                with AuthDAO(conn) as a_dao:
                    customer = a_dao.find_user(email, current_app.config['CUST_AUTH'])

                    # Invalid email
                    if customer is None:
                        raise ApplicationError(code=401, message=current_app.config['INVALID_USERNAME_OR_PASSWORD_MESSAGE'])

                    # Invalid password
                    if customer['password'] != hashlib.sha256(password.encode()).hexdigest():
                        raise ApplicationError(code=401, message=current_app.config['INVALID_USERNAME_OR_PASSWORD_MESSAGE'])

                    logger.info(f"Customer with c_id:{customer['c_id']} logged in")

            return customer['c_id']

        except Error as err:
            logger.error(f'Customer login: MySQL error {err}')
            raise DataBaseException(current_app.config['LOGIN_ERROR_MESSAGE'])

    @staticmethod
    def generate_token(cust_id):
        additional_claims = {
            'role': current_app.config['CUSTOMER']
        }
        token = create_access_token(identity=cust_id, additional_claims=additional_claims)
        return token
