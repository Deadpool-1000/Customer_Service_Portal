from src.handlers.authentication.logout.BLOCKLIST import BLOCKLIST


class LogoutHandler:
    @staticmethod
    def logout(jti):
        BLOCKLIST.add(jti)

