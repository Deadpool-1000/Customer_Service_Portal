import logging
import shortuuid
import hashlib
from utils.exceptions import InvalidUsernameOrPasswordException, AlreadyExistsException

logger = logging.getLogger("auth_dao")

CREATE_TABLE_CUST_AUTH = 'CREATE TABLE IF NOT EXISTS cust_auth (cid text PRIMARY KEY, email TEXT UNIQUE, password TEXT)'
CREATE_TABLE_EMP = 'CREATE TABLE IF NOT EXISTS emp_auth (e_id TEXT PRIMARY KEY, email TEXT UNIQUE, password TEXT)'
FIND_USER_QUERY = 'SELECT * FROM {} WHERE email = ?'
INVALID_USERNAME_LOG = 'Invalid Username detected'
INVALID_PASSWORD_LOG = 'Invalid password detected'
FIND_DEPT_BY_DEPTID = 'SELECT dept_name from dept WHERE dept_id=?'
ALREADY_EXISTS_EXCEPTION = 'Email already exists, please try a different email'
INSERT_INTO_CUSTOMER_AUTH_TABLE = 'INSERT INTO cust_auth VALUES(?, ?, ?)'
INVALID_USERNAME_OR_PASSWORD = 'Invalid Username or password'


class AuthDAO:
    singleton = 1

    def __init__(self, conn):
        self.cur = conn.cursor()
        if self.singleton != 0:
            self.cur.execute(CREATE_TABLE_CUST_AUTH)
            self.cur.execute(CREATE_TABLE_EMP)
            self.singleton -= 1

    def find_user(self, email, table_name):
        return self.cur.execute(FIND_USER_QUERY.format(table_name), (email, )).fetchone()

    def login_user(self, email, password, table_name):
        found_user = self.find_user(email=email, table_name=table_name)
        if found_user is None:
            logger.info(INVALID_USERNAME_LOG)
            raise InvalidUsernameOrPasswordException(INVALID_USERNAME_OR_PASSWORD)

        if found_user[2] != hashlib.sha256(password.encode()).hexdigest():
            logger.info(INVALID_PASSWORD_LOG)
            raise InvalidUsernameOrPasswordException(INVALID_USERNAME_OR_PASSWORD)

        # 'cid', 'email', 'password'
        return found_user[0]

    def customer_signup(self, email, password) -> str:
        rws = self.find_user(email, table_name='cust_auth')
        if rws is not None:
            logger.info(ALREADY_EXISTS_EXCEPTION)
            raise AlreadyExistsException(ALREADY_EXISTS_EXCEPTION)
        cust_id: str = shortuuid.ShortUUID().random(length=5)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cur.execute(INSERT_INTO_CUSTOMER_AUTH_TABLE, (cust_id, email, hashed_password))
        return cust_id
