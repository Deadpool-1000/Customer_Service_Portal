import logging
from flask_jwt_extended import create_access_token
from mysql.connector import Error

from src.DBUtils.connection.database_connection import DatabaseConnection
from src.DBUtils.auth.authdao import AuthDAO
from src.DBUtils.customer.customerdao import CustomerDAO
from src.authentication.config.auth_config_loader import AuthConfig
from src.utils.exceptions.exceptions import DataBaseException

logger = logging.getLogger('main.login')


class CustomerLoginHandler:
    @staticmethod
    def login_customer(email, password):
        try:
            with DatabaseConnection() as conn:

                a_dao = AuthDAO(conn)
                c_id = a_dao.login_user(email, password, AuthConfig.CUST_AUTH)
                logger.info(f"Employee with c_id:{c_id} logged in")

            return c_id
        except Error as err:
            logger.error(f'Customer login: MySQL error {err}')
            raise DataBaseException('There was some problem with Database.')

    @staticmethod
    def generate_token(cust_id):
        additional_claims = {
            'role': AuthConfig.CUSTOMER
        }
        token = create_access_token(identity=cust_id, additional_claims=additional_claims)
        return token
