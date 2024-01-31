import hashlib
import logging
import shortuuid
from src.DBUtils.config.queries_config_loader import QueriesConfig

logger = logging.getLogger("main.auth_dao")


class AuthDAO:
    singleton = 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            return False
        self.cur.close()

    def __init__(self, conn):
        self.cur = conn.cursor(dictionary=True)
        if self.singleton != 0:
            self.cur.execute(QueriesConfig.CREATE_TABLE_CUST_AUTH)
            self.cur.execute(QueriesConfig.CREATE_TABLE_EMP)
            self.singleton -= 1

    def find_user(self, email, table_name):
        self.cur.execute(QueriesConfig.FIND_USER_QUERY.format(table_name), {
            'email': email
        })
        return self.cur.fetchone()

    def add_customer_auth_details(self, email, password) -> str:
        cust_id = shortuuid.ShortUUID().random(5)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cur.execute(QueriesConfig.INSERT_INTO_CUSTOMER_AUTH_TABLE, (cust_id, email, hashed_password))
        return cust_id
