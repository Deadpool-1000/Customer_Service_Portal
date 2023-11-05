from os import system
from DBUtils.connection.database_connection import DatabaseConnection
from DBUtils.auth.authdao import AuthDAO
from DBUtils.customer.customerdao import CustomerDAO
from utils.exceptions import AlreadyExistsException, InvalidCustomerIDException
from utils.input_utils import input_customer_details

PLEASE_TRY_AGAIN = "Please Try Again"


class Signup:
    @staticmethod
    def customer_signup():
        email, fullname, phn_num, address, password = input_customer_details()
        # email, fullname, phn_num, address, password = "abc", "abc", "abc", "abc", "abc"
        try:
            with DatabaseConnection() as conn:
                auth_dao = AuthDAO(conn)
                cust_id = auth_dao.customer_signup(email, password)
                cust_dao = CustomerDAO(conn)
                cust_dao.add_customer_details(cust_id, fullname, phn_num, address)
            return True
        except InvalidCustomerIDException as ie:
            system('cls')
            print(ie)
            print(PLEASE_TRY_AGAIN)
            return False
        except AlreadyExistsException as ae:
            system('cls')
            print(ae)
            print(PLEASE_TRY_AGAIN)
            return False
