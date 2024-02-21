import hashlib
import pymysql
from flask import current_app
from flask_jwt_extended import create_access_token


from src.dbutils.auth.auth_dao import AuthDAO
from src.dbutils.connection.database_connection import DatabaseConnection
from src.utils.exceptions.exceptions import DataBaseException, ApplicationError


class CustomerLoginHandler:
    @staticmethod
    def login_customer(email, password):
        """Takes email and password verifies with database and returns the customer identification number"""
        try:
            with (DatabaseConnection() as conn):
                with AuthDAO(conn) as a_dao:
                    customer = a_dao.find_user(email, current_app.config['CUST_AUTH'])

                    # Invalid email
                    if customer is None:
                        current_app.logger.error(f"Customer Login: Invalid email {email} provided.")
                        raise ApplicationError(code=401,
                                               message=current_app.config['INVALID_USERNAME_OR_PASSWORD_MESSAGE'])

                    # Invalid password
                    if customer['password'] != hashlib.sha256(password.encode()).hexdigest():
                        current_app.logger.error(f"Customer with email {email} provided wrong password.")
                        raise ApplicationError(code=401,
                                               message=current_app.config['INVALID_USERNAME_OR_PASSWORD_MESSAGE'])

                    current_app.logger.info(f"Customer with c_id:{customer['c_id']} logged in")

            return customer['c_id']

        except pymysql.Error as e:
            current_app.logger.error(f'Customer login: {e.args[0]}: {e.args[1]}')
            raise DataBaseException(current_app.config['LOGIN_ERROR_MESSAGE'])

    @staticmethod
    def generate_token(cust_id):
        """Generates JWT access tokens based on customer identification number"""
        additional_claims = {
            'role': current_app.config['CUSTOMER']
        }
        token = create_access_token(identity=cust_id, additional_claims=additional_claims)
        return token
