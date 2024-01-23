import logging
from mysql.connector import Error

from src.DBUtils.connection.database_connection import DatabaseConnection
from src.DBUtils.auth.authdao import AuthDAO
from src.DBUtils.customer.customerdao import CustomerDAO
from src.utils.exceptions import DataBaseException

logger = logging.getLogger('main.customer_signup_handler')


class CustomerSignupHandler:
    @staticmethod
    def signup_customer(email, fullname, phn_num, address, password):
        try:
            with DatabaseConnection() as conn:
                auth_dao = AuthDAO(conn)
                cust_id = auth_dao.customer_signup(email, password)

                cust_dao = CustomerDAO(conn)
                cust_dao.add_customer_details(cust_id, fullname, phn_num, address)

                logger.info(f'New Customer signup with name:{fullname} and email:{email}')
            return True
        except Error as e:
            logger.error(f'Database error during customer signup {e}')
            raise DataBaseException('There was some problem signing up. Please try again later.')