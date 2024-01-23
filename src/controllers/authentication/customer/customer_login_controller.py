from flask_smorest import abort
from src.handlers.authentication.customer.customer_login_handler import CustomerLoginHandler
from src.utils.exceptions.exceptions import InvalidUsernameOrPasswordException, DataBaseException


class CustomerLoginController:
    @staticmethod
    def login(cust_data):
        try:
            email = cust_data['email']
            password = cust_data['password']

            customer = CustomerLoginHandler.login_customer(email, password)
            token = CustomerLoginHandler.generate_token(cust_id=customer['c_id'])
            return {
                'token': token
            }

        except InvalidUsernameOrPasswordException as e:
            return abort(401, message='Invalid Username or Password provided.')

        except DataBaseException:
            return abort(500, message='There was some problem while logging you in. Please try again later')
