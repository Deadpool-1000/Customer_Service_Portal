from flask_smorest import abort

from src.utils.exceptions import AlreadyExistsException, DataBaseException
from src.handlers.authentication.customer.customer_signup_handler import CustomerSignupHandler
from src.schemas.user import SuccessSchema


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
                success_message = SuccessSchema().load({
                    'message': 'Successfully registered'
                })
                return success_message

        except AlreadyExistsException as ae_exception:
            abort(409, message=str(ae_exception))

        except DataBaseException as db_exception:
            abort(500, message=str(db_exception))
