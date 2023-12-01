import pytest
import hashlib
from src.DBUtils.auth.authdao import AuthDAO
from src.utils.exceptions.exceptions import InvalidUsernameOrPasswordException, AlreadyExistsException


@pytest.fixture
def auth_dao(mock_sqlite3_conn):
    a = AuthDAO(mock_sqlite3_conn)
    return a


@pytest.mark.usefixtures('my_config_loader')
class TestAuthDAO:
    def test_login_user_with_success(self, auth_dao, mock_sqlite3_cur):
        password = hashlib.sha256("Abcdef@2".encode()).hexdigest()
        mock_sqlite3_cur.execute.return_value.fetchone.return_value = ('111', 'test_email@gmail.com', password)
        return_user = auth_dao.login_user('test_email@gmail.com', "Abcdef@2", 'employee')
        assert return_user == '111'

    @pytest.mark.parametrize(('email', 'password'), [('test_gmail@gmail.com', 'Abcdef@2')])
    def test_login_user_with_wrong_password(self, auth_dao, mock_sqlite3_cur, email, password):
        hashed_password = hashlib.sha256("Abcdefg@2".encode()).hexdigest()
        mock_sqlite3_cur.execute.return_value.fetchone.return_value = ('111', 'test_email@gmail.com', hashed_password)
        with pytest.raises(InvalidUsernameOrPasswordException):
            auth_dao.login_user(email, password, 'employee')

    @pytest.mark.parametrize(('email', 'password'), [('test_wrong@gmail.com', 'Abcdefg@2')])
    def test_login_user_with_wrong_email(self, auth_dao, mock_sqlite3_cur, email, password):
        mock_sqlite3_cur.execute.return_value.fetchone.return_value = None
        with pytest.raises(InvalidUsernameOrPasswordException):
            auth_dao.login_user(email, password, 'employee')

    def test_customer_signup_success(self, auth_dao, mock_sqlite3_cur):
        mock_sqlite3_cur.execute.return_value.fetchone.return_value = None
        ret_val = auth_dao.customer_signup('abc@gmail.com', 'test_password')
        assert ret_val is not None

    def test_customer_signup_with_already_exists(self, mock_sqlite3_cur, auth_dao):
        mock_sqlite3_cur.execute.return_value.fetchone.return_value = ('111', 'test_email@gmail.com', 'Abcdef@2')
        with pytest.raises(AlreadyExistsException):
            auth_dao.customer_signup('abc@gmail.com', 'test_password')
