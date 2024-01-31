from flask_smorest import abort
from src.handlers.authentication.customer.customer_login_handler import CustomerLoginHandler
from src.utils.exceptions.exceptions import DataBaseException, ApplicationError


class CustomerLoginController:
    @staticmethod
    def login(cust_data):
        try:
            email = cust_data['email']
            password = cust_data['password']

            c_id = CustomerLoginHandler.login_customer(email, password)
            token = CustomerLoginHandler.generate_token(cust_id=c_id)
            return {
                'token': token
            }

        except ApplicationError as ae:
            return abort(ae.code, message=ae.message)

        except DataBaseException as db:
            return abort(500, message=str(db))
