from flask import current_app
from flask_smorest import abort

from src.utils.exceptions import ApplicationError, DataBaseException
from src.handlers.authentication.customer.customer_signup_handler import CustomerSignupHandler


class CustomerSignupController:
    @staticmethod
    def signup(cust_data):
        email = cust_data['email']
        password = cust_data['password']
        full_name = cust_data['full_name']
        phn_num = cust_data['phn_num']
        address = cust_data['address']

        try:
            success = CustomerSignupHandler.signup_customer(email=email, password=password, fullname=full_name, phn_num=phn_num, address=address)
            if success:
                return {
                    'message': current_app.config['REGISTER_SUCCESS_MESSAGE']
                }

        except ApplicationError as ae:
            abort(ae.code, message=ae.message)

        except DataBaseException as db_exception:
            abort(500, message=str(db_exception))
