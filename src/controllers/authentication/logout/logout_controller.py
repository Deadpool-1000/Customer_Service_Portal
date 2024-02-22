from datetime import datetime

from flask import current_app
from flask_smorest import abort

from src.handlers.authentication.logout.logout_handler import LogoutHandler
from src.utils.exceptions import DataBaseException


logger = current_app.logger


class LogoutController:
    @staticmethod
    def logout(token):
        try:
            jti = token['jti']
            exp = datetime.utcfromtimestamp(token['exp'])
            LogoutHandler.logout(jti, exp)
            LogoutHandler.clear_expired_tokens()
            logger.info(f"{token['sub']} logged out.")
            return {
                "message": current_app.config['LOGOUT_SUCCESS_MESSAGE']
            }
        except DataBaseException as db:
            abort(500, message=str(db))
