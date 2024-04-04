from src.dbutils.auth.auth_dao import AuthDAO
from src.dbutils.connection import DatabaseConnection


class UserHandler:
    @staticmethod
    def get_profile(user_id, role):
        with DatabaseConnection() as conn:
            with AuthDAO(conn) as a_dao:
                return a_dao.get_user_profile(user_id, role)
