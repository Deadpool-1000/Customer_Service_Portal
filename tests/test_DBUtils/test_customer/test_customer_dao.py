import pytest
from src.DBUtils.customer.customerdao import CustomerDAO
from src.utils.exceptions.exceptions import InvalidCustomerIDException


@pytest.fixture
def customer_dao(mock_sqlite3_conn):
    c = CustomerDAO(mock_sqlite3_conn)
    return c


class TestCustomerDAO:
    def test_get_customer_details_by_id_success(self, mock_sqlite3_cur, customer_dao):
        mock_sqlite3_cur.execute.return_value.fetchone.return_value = ('111', 'test_full_name', '9898989889', 'Abc street, some city')
        assert customer_dao.get_customer_details_by_id(111) == ('111', 'test_full_name', '9898989889', 'Abc street, some city')

    def test_get_customer_details_by_id_fail(self, mock_sqlite3_cur, customer_dao):
        mock_sqlite3_cur.execute.return_value.fetchone.return_value = None
        with pytest.raises(InvalidCustomerIDException):
            customer_dao.get_customer_details_by_id(111)

    # Not sure how to test this:
    # def test_add_customer_details(self, customer_dao, mock_sqlite3_cur):
    #     customer_dao.add_customer_details(1111, 'test_fullname', '9898989822', 'abc street, some city')
