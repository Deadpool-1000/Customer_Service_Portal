import logging
import sqlite3
from os import system
from authentication.config.auth_config_loader import AuthConfig
from DBUtils.connection.database_connection import DatabaseConnection
from DBUtils.auth.authdao import AuthDAO
from DBUtils.customer.customerdao import CustomerDAO
from utils.exceptions import AlreadyExistsException, InvalidCustomerIDException
from utils.input_utils import input_customer_details

logger = logging.getLogger('main.signup')


class Signup:
    @staticmethod
    def customer_signup():
        email, fullname, phn_num, address, password = input_customer_details()
        try:
            with DatabaseConnection() as conn:
                auth_dao = AuthDAO(conn)
                cust_id = auth_dao.customer_signup(email, password)
                cust_dao = CustomerDAO(conn)
                cust_dao.add_customer_details(cust_id, fullname, phn_num, address)
                logger.info(f'New Customer signup with name:{fullname} and email:{email}')
            return True
        except InvalidCustomerIDException as ie:
            system('cls')
            logger.error(f'Invalid Customer Id detected with email:{email}')
            print(ie)
            print(AuthConfig.PLEASE_TRY_AGAIN)
            return False
        except AlreadyExistsException as ae:
            logger.error(f'Email Already exists: {email}')
            system('cls')
            print(ae)
            print(AuthConfig.PLEASE_TRY_AGAIN)
            return False
        except sqlite3.Error as err:
            logger.error(f'Customer login: {err.sqlite_errorname}')
            print('There was a problem signing you up')
            print('Please try again after some time.')
            return None
