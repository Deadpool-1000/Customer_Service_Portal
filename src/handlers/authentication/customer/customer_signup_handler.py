import logging
from mysql.connector import Error

from src.DBUtils.connection.database_connection import DatabaseConnection
from src.DBUtils.auth.authdao import AuthDAO
from src.DBUtils.customer.customerdao import CustomerDAO
from src.utils.exceptions import DataBaseException, AlreadyExistsException, ApplicationError

logger = logging.getLogger('main.customer_signup_handler')

SIGNUP_ERROR_MESSAGE = 'There was some problem signing up. Please try again later.'
ALREADY_EXIST_MESSAGE = 'Email taken. Please try again later.'


class CustomerSignupHandler:
    @staticmethod
    def signup_customer(email, fullname, phn_num, address, password):
        try:
            with DatabaseConnection() as conn:
                with AuthDAO(conn) as a_dao:
                    cust_id = a_dao.customer_signup(email, password)

                with CustomerDAO(conn) as c_dao:
                    c_dao.add_customer_details(cust_id, fullname, phn_num, address)

                logger.info(f'New Customer signup with name:{fullname} and email:{email}')
            return True

        except AlreadyExistsException as ae:
            logger.error(f'Email taken for email {email}')
            raise ApplicationError(code=409, message=ALREADY_EXIST_MESSAGE)

        except Error as e:
            logger.error(f'Database error during customer signup {e}')
            raise DataBaseException(SIGNUP_ERROR_MESSAGE)
