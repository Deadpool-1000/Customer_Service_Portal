from src.handlers.authentication.logout.BLOCKLIST import BLOCKLIST


class LogoutHandler:
    """Add token to blocklist"""
    @staticmethod
    def logout(jti):
        BLOCKLIST.add(jti)
