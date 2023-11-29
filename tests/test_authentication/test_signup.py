import pytest
import sqlite3
from src.authentication.signup import Signup
from src.utils.exceptions.exceptions import AlreadyExistsException


@pytest.fixture
def mock_input_customer_details(mocker):
    mocker.patch(
        'src.authentication.signup.input_customer_details', lambda: (
            'test_email@test.com',
            'test_full_name',
            'test_ph_num',
            'test_address',
            'test_password'
        )
    )


class TestSignup:
    def test_customer_signup_success(self, mock_input_customer_details, mock_auth_dao, mock_customer_dao):
        mock_auth_dao.customer_signup = lambda email, password: 1
        mock_customer_dao.add_customer_details = lambda cust_id, fullname, phn_num, address: None
        success = Signup.customer_signup()
        assert success is True

    def test_customer_signup_fail_with_already_exists(self, mock_input_customer_details, mock_auth_dao):
        mock_auth_dao.customer_signup.side_effect = AlreadyExistsException
        success = Signup.customer_signup()
        assert success is False

    def test_customer_signup_fail_with_sqlite3_error(self, mock_input_customer_details, mock_auth_dao):
        mock_auth_dao.customer_signup.side_effect = sqlite3.Error
        success = Signup.customer_signup()
        assert success is None
