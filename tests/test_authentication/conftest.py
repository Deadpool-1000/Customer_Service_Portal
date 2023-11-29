import pytest


@pytest.fixture
def mock_database_conn(mocker):
    mock_db = mocker.MagicMock()
    mocker.patch('src.authentication.login.DatabaseConnection', mock_db)
    mocker.patch('src.authentication.signup.DatabaseConnection', mock_db)


@pytest.fixture
def mock_employee_dao(mocker, mock_database_conn):
    mock_emp = mocker.MagicMock()
    mocker.patch('src.authentication.login.EmployeeDAO', mock_emp)
    return mock_emp()


@pytest.fixture
def mock_customer_dao(mocker, mock_database_conn):
    mock_cust = mocker.MagicMock()
    mocker.patch('src.authentication.login.CustomerDAO', mock_cust)
    mocker.patch('src.authentication.signup.CustomerDAO', mock_cust)
    return mock_cust()


@pytest.fixture
def mock_auth_dao(mocker, mock_database_conn):
    mock_auth = mocker.MagicMock()
    mocker.patch('src.authentication.login.AuthDAO', mock_auth)
    mocker.patch('src.authentication.signup.AuthDAO', mock_auth)
    return mock_auth()
