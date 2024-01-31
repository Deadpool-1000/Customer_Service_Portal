from src.handlers.authentication.logout.logout_handler import LogoutHandler
from src.handlers import CSMConfig


class LogoutController:
    @staticmethod
    def logout(token):
        jti = token['jti']
        LogoutHandler.logout(jti)
        return {
            "message": CSMConfig.LOGOUT_SUCCESS_MESSAGE
        }
