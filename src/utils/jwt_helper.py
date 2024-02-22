from src.dbutils.auth.auth_dao import AuthDAO
from src.dbutils.connection import DatabaseConnection


def is_jwt_in_blocklist(jti):
    with DatabaseConnection() as conn:
        with AuthDAO(conn) as a_dao:
            token = a_dao.get_token_by_jti(jti)

    return token is not None
