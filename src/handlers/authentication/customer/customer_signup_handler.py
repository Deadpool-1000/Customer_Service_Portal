import logging
import pymysql
from flask import current_app

from src.dbutils.auth.auth_dao import AuthDAO
from src.dbutils.connection.database_connection import DatabaseConnection
from src.dbutils.customer.customer_dao import CustomerDAO
from src.utils.exceptions import DataBaseException, ApplicationError

logger = logging.getLogger('main.customer_signup_handler')


class CustomerSignupHandler:
    @staticmethod
    def signup_customer(email, fullname, phn_num, address, password):
        """Add customer details to database. Also, verifies if the email is already in use."""
        try:
            with DatabaseConnection() as conn:
                with AuthDAO(conn) as a_dao:
                    already_exists = a_dao.find_user(email, current_app.config['CUST_AUTH'])
                    if already_exists:
                        current_app.logger.error(f'Customer tried to signup with an already taken email {email}.')
                        raise ApplicationError(code=409, message=current_app.config['EMAIL_TAKEN_MESSAGE'])

                    # Add customer to auth table
                    cust_id = a_dao.add_customer_auth_details(email, password)

                # Add customer details
                with CustomerDAO(conn) as c_dao:
                    c_dao.add_customer_details(cust_id, fullname, phn_num, address)

                logger.info(f'New Customer signup with name:{fullname} and email:{email}')
            return True

        except pymysql.Error as e:
            logger.error(f'Database error during customer signup {e.args[0]}: {e.args[1]}')
            raise DataBaseException(current_app.config['SIGNUP_ERROR_MESSAGE'])
