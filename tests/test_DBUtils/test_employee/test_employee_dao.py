import pytest
from src.DBUtils.employee.employeedao import EmployeeDAO
from src.utils.exceptions.exceptions import InvalidDepartmentIDException, InvalidEmployeeIDException


@pytest.fixture
def emp_dao(mock_sqlite3_conn):
    e = EmployeeDAO(mock_sqlite3_conn)
    return e


class TestEmployeeDAO:
    def test_get_employee_details_by_id_with_success(self, emp_dao, mock_sqlite3_cur):
        mock_sqlite3_cur.execute.return_value.fetchone.return_value = ('c_id', 'full_name', 'phn_num', 'address', 'dept_id', 'designation')
        ret_val = emp_dao.get_employee_details_by_id(1111)
        assert ret_val == ('c_id', 'full_name', 'phn_num', 'address', 'dept_id', 'designation')

    def test_get_employee_details_by_id_with_failure(self, emp_dao, mock_sqlite3_cur):
        mock_sqlite3_cur.execute.return_value.fetchone.return_value = None
        with pytest.raises(InvalidEmployeeIDException):
            emp_dao.get_employee_details_by_id(1111)

    def test_get_department_by_id_with_success(self, emp_dao, mock_sqlite3_cur):
        mock_sqlite3_cur.execute.return_value.fetchone.return_value = ('1', 'sales')
        ret_val = emp_dao.get_department_by_id(1)
        assert ret_val == ('1', 'sales')

    def test_get_department_by_id_with_failure(self, emp_dao, mock_sqlite3_cur):
        mock_sqlite3_cur.execute.return_value.fetchone.return_value = None
        with pytest.raises(InvalidDepartmentIDException):
            emp_dao.get_department_by_id(1)
