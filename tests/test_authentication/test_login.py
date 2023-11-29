import sqlite3
import pytest
from src.authentication.login import Login
from src.utils.data_containers.named_tuples import Employee, Customer
from src.utils.exceptions.exceptions import InvalidUsernameOrPasswordException, InvalidEmployeeIDException, InvalidDepartmentIDException


valid_sample_users_credentials = [
        {
            'e_id': 1,
            'name': 'test1',
            'phn_num': 'test number1',
            'address': 'test address1',
            'email': 'test1@gmail.com',
            'dept_id': 1,
            'dept_name': 'sales',
            'designation': 'employee',
            'password': 'Abcdef@2'
        },
        {
            'e_id': 2,
            'name': 'test2',
            'phn_num': 'test number2',
            'address': 'test address2',
            'email': 'test2@gmail.com',
            'dept_id': 2,
            'dept_name': 'IT',
            'designation': 'employee',
            'password': 'Abcdef@2'
        },
        {
            'c_id': 3,
            'name': 'test3',
            'phn_num': 'test number3',
            'address': 'test address3',
            'email': 'test3@gmail.com',
            'password': 'Abcdef@2'
        }
]


class TestLogin:
    @pytest.mark.parametrize('credentials', [('test1@gmail.com', 'Abcdef@2')])
    def test_employee_login_with_valid_uname_and_password(self, mocker, credentials, mock_auth_dao, mock_employee_dao):
        mocker.patch('src.authentication.login.input_email_password', lambda: credentials)

        mock_auth_dao.login_user = lambda email, password, type_of_login: 1

        current_employee = valid_sample_users_credentials[0]
        mock_employee_dao.get_employee_details_by_id = lambda e_id: (
            current_employee['e_id'], current_employee['name'], current_employee['phn_num'],
            current_employee['dept_id'],
            current_employee['address'],
            current_employee['designation']
        )
        mock_employee_dao.get_department_by_id = lambda dept_id: (dept_id, 'sales')

        employee = Login.employee_login()
        assert employee == Employee(name=current_employee['name'], e_id=current_employee['e_id'], phn_num=current_employee['phn_num'], address=current_employee['address'], email=current_employee['email'], dept_id=current_employee['dept_id'], dept_name=current_employee['dept_name'], designation=current_employee['designation'])

    @pytest.mark.parametrize('credentials', [('test_wrong@gmail.com', 'wrong_pass')])
    def test_employee_login_with_invalid_uname_or_password(self, mocker, credentials, mock_auth_dao):
        mocker.patch('src.authentication.login.input_email_password', lambda: credentials)

        mock_auth_dao.login_user.side_effect = InvalidUsernameOrPasswordException

        ret_val = Login.employee_login()
        assert ret_val is False

    @pytest.mark.parametrize('credentials', [('test_wrong@gmail.com', 'wrong_pass')])
    def test_employee_login_with_invalid_e_id(self, mocker, credentials, mock_auth_dao, mock_employee_dao):
        mocker.patch('src.authentication.login.input_email_password', lambda: credentials)
        mock_auth_dao.login_user = lambda email, password, type_of_login: 1

        mock_employee_dao.get_employee_details_by_id.side_effect = InvalidEmployeeIDException

        ret_val = Login.employee_login()
        assert ret_val is False

    @pytest.mark.parametrize('credentials', [('test_wrong@gmail.com', 'wrong_pass')])
    def test_employee_login_fail_with_invalid_dept_id(self, mocker, credentials, mock_auth_dao, mock_employee_dao):
        mocker.patch('src.authentication.login.input_email_password', lambda: credentials)

        mock_auth_dao.login_user = lambda email, password, type_of_login: 1

        current_employee = valid_sample_users_credentials[0]
        mock_employee_dao.get_employee_details_by_id = lambda e_id: (
            current_employee['e_id'], current_employee['name'], current_employee['phn_num'],
            current_employee['dept_id'],
            current_employee['address'],
            current_employee['designation']
        )
        mock_employee_dao.get_department_by_id.side_effect = InvalidDepartmentIDException

        success = Login.employee_login()
        assert success is False

    @pytest.mark.parametrize('credentials', [('test_wrong@gmail.com', 'wrong_pass')])
    def test_employee_login_fail_with_sqlite3_error(self, mocker, credentials, mock_auth_dao, mock_employee_dao):
        mocker.patch('src.authentication.login.input_email_password', lambda: credentials)

        mock_auth_dao.login_user = lambda email, password, type_of_login: 1

        current_employee = valid_sample_users_credentials[0]
        mock_employee_dao.get_employee_details_by_id = lambda e_id: (
            current_employee['e_id'], current_employee['name'], current_employee['phn_num'],
            current_employee['dept_id'],
            current_employee['address'],
            current_employee['designation']
        )
        mock_employee_dao.get_department_by_id.side_effect = sqlite3.Error

        success = Login.employee_login()
        assert success is None

    @pytest.mark.parametrize('credentials', [('test3@gmail.com', 'Abcdef@2')])
    def test_customer_login_with_valid_credentials(self, mocker, credentials, mock_auth_dao, mock_customer_dao):
        mocker.patch('src.authentication.login.input_email_password', lambda: credentials)
        Login.customer_login()
        mock_auth_dao.login_user = lambda email, password, type_of_login: 2

        customer = valid_sample_users_credentials[2]
        mock_customer_dao.get_customer_details_by_id = lambda c_id: (
            customer['c_id'],
            customer['name'],
            customer['phn_num'],
            customer['address'],
        )
        ret_val = Login.customer_login()
        expected_val = Customer(
            name=customer['name'],
            c_id=customer['c_id'],
            phn_num=customer['phn_num'],
            address=customer['address'],
            email=customer['email']
        )

        assert ret_val == expected_val

    @pytest.mark.parametrize('credentials', [('wrong_email@gmail.com', 'wrong_pass')])
    def test_customer_login_with_wrong_credentials(self, mocker, credentials, mock_auth_dao):
        mocker.patch('src.authentication.login.input_email_password', lambda: credentials)

        mock_auth_dao.login_user.side_effect = InvalidUsernameOrPasswordException

        ret_val = Login.customer_login()

        assert ret_val is False

    @pytest.mark.parametrize('credentials', [('test3@gmail.com', 'Abcdef@2')])
    def test_customer_login_with_sqlite_error(self, mocker, credentials, mock_auth_dao):
        mocker.patch('src.authentication.login.input_email_password', lambda: credentials)

        mock_auth_dao.login_user.side_effect = sqlite3.Error

        ret_val = Login.customer_login()

        assert ret_val is None
