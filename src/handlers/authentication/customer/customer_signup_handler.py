import logging
from mysql.connector import Error

from src.DBUtils.connection.database_connection import DatabaseConnection
from src.DBUtils.auth.authdao import AuthDAO
from src.DBUtils.customer.customerdao import CustomerDAO
from src.utils.exceptions import DataBaseException, AlreadyExistsException, ApplicationError
from src.handlers import CSMConfig

logger = logging.getLogger('main.customer_signup_handler')

SIGNUP_ERROR_MESSAGE = 'There was some problem signing up. Please try again later.'
ALREADY_EXIST_MESSAGE = 'Email taken. Please try again later.'
EMAIL_TAKEN_MESSAGE = 'Email Already in use. Please try again with a new email.'


class CustomerSignupHandler:
    @staticmethod
    def signup_customer(email, fullname, phn_num, address, password):
        try:
            with DatabaseConnection() as conn:
                with AuthDAO(conn) as a_dao:

                    already_exists = a_dao.find_user(email, CSMConfig.CUST_AUTH)
                    if already_exists:
                        raise ApplicationError(code=409, message=EMAIL_TAKEN_MESSAGE)

                    # Add customer to auth table
                    cust_id = a_dao.add_customer_auth_details(email, password)

                # Add customer details
                with CustomerDAO(conn) as c_dao:
                    c_dao.add_customer_details(cust_id, fullname, phn_num, address)

                logger.info(f'New Customer signup with name:{fullname} and email:{email}')
            return True

        except Error as e:
            logger.error(f'Database error during customer signup {e}')
            raise DataBaseException(SIGNUP_ERROR_MESSAGE)
