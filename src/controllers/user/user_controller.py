from flask import current_app

from src.handlers.user.user_handler import UserHandler
from flask_smorest import abort

from src.utils.exceptions import DataBaseException


class UserController:
    @staticmethod
    def get_profile(user_id, role):
        try:
            return UserHandler.get_profile(user_id, role)
        except DataBaseException as db:
            abort(500, message=str(db))

    @staticmethod
    def put_customer_profile(user_id, new_user_data):
        try:
            if user_id != new_user_data['c_id']:
                abort(400, message=current_app.config['CUSTOMER_ID_MISMATCH'])

            UserHandler.put_customer_profile(new_user_data)

            return {
                'message': current_app.config['PROFILE_UPDATE_SUCCESS_MESSAGE']
            }
        except DataBaseException as db:
            abort(500, message=str(db))
