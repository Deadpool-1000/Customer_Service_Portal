from flask import current_app
from src.handlers.authentication.logout.logout_handler import LogoutHandler


class LogoutController:
    @staticmethod
    def logout(token):
        jti = token['jti']
        LogoutHandler.logout(jti)
        return {
            "message": current_app.config['LOGOUT_SUCCESS_MESSAGE']
        }
