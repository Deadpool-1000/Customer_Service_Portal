from flask import current_app

from src.handlers.authentication.logout.logout_handler import LogoutHandler

logger = current_app.logger


class LogoutController:
    @staticmethod
    def logout(token):
        jti = token['jti']
        LogoutHandler.logout(jti)
        logger.info(f"{token['sub']} logged out.")
        return {
            "message": current_app.config['LOGOUT_SUCCESS_MESSAGE']
        }
