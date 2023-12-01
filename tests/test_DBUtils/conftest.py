import pytest


@pytest.fixture()
def mock_sqlite3_cur(mocker):
    mock_cur = mocker.Mock()
    return mock_cur


@pytest.fixture()
def mock_sqlite3_conn(mocker, mock_sqlite3_cur):
    mock_conn = mocker.Mock()
    mock_conn.cursor.return_value = mock_sqlite3_cur
    return mock_conn
