import pymysql
from flask import current_app

from src.dbutils.auth.auth_dao import AuthDAO
from src.dbutils.connection import DatabaseConnection
from src.handlers.authentication.logout.BLOCKLIST import BLOCKLIST
from src.utils.exceptions import DataBaseException


class LogoutHandler:
    """Add token to blocklist"""
    @staticmethod
    def logout(jti, exp):
        try:
            with DatabaseConnection() as conn:
                with AuthDAO(conn) as a_dao:
                    a_dao.add_token_to_blocklist(jti, exp)

        except pymysql.Error as e:
            print(e.args)
            current_app.logger.error(f'Error during logout: {e.args[0]}: {e.args[1]}')
            raise DataBaseException(current_app.config['LOGOUT_ERROR_MESSAGE']) from e
        except pymysql.IntegrityError as e:
            print(e.args)
            current_app.logger.error(f'Logout integrity error: {e.args[0]}: {e.args[1]}')
            raise DataBaseException(current_app.config['LOGOUT_ERROR_MESSAGE']) from e

    @staticmethod
    def clear_expired_tokens():
        try:
            with DatabaseConnection() as conn:
                with AuthDAO(conn) as a_dao:
                    a_dao.clear_tokens()
        except pymysql.Error as e:
            current_app.logger.error(f'Error during clearing expired tokens procedure: {e.args[0]}: {e.args[1]}')
            raise DataBaseException(current_app.config['LOGOUT_ERROR_MESSAGE']) from e
