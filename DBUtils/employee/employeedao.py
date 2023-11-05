import logging
import sqlite3
import shortuuid
from utils.exceptions import NoDepartmentsException

from utils.exceptions import InvalidEmployeeIDException, InvalidDepartmentIDException

CREATE_TABLE_DEPT_DETAILS = "CREATE TABLE IF NOT EXISTS dept_details(dept_id TEXT PRIMARY KEY, dept_name TEXT)"
CREATE_TABLE_EMP_DETAILS = "CREATE TABLE IF NOT EXISTS emp_details (e_id TEXT PRIMARY KEY, full_name TEXT, phn_num TEXT, dept_id TEXT, address TEXT, designation TEXT, FOREIGN KEY(dept_id) REFERENCES dept_details(dept_id), FOREIGN KEY(e_id) REFERENCES emp_auth(e_id))"
GET_EMPLOYEE_DETAILS_BY_ID = "SELECT * FROM emp_details WHERE e_id = ?"
DEPT_TABLE_MAPPING_QUERY = "SELECT * FROM dept_details"
GET_DEPT_DETAILS_BY_ID = "SELECT * FROM dept_details WHERE dept_id = ?"
INVALID_DEPT_ID = "Invalid department id encountered"
INVALID_EMP_ID = "Invalid employee id encountered"


logger = logging.getLogger('main.employee_dao')
THERE_WAS_SOME_PROBLEM = "There was some problem."


class EmployeeDAO:
    singleton = 1

    def __init__(self, conn):
        self.cur = conn.cursor()
        if self.singleton != 0:
            self.cur.execute(CREATE_TABLE_DEPT_DETAILS)
            self.cur.execute(CREATE_TABLE_EMP_DETAILS)
            conn.commit()
            self.singleton -= 1

    def get_employee_details_by_id(self, e_id):
        rws = self.cur.execute(GET_EMPLOYEE_DETAILS_BY_ID, (e_id,)).fetchone()
        if rws is None:
            logger.info(INVALID_EMP_ID)
            raise InvalidEmployeeIDException(THERE_WAS_SOME_PROBLEM)
        # 'c_id', 'full_name', 'phn_num', 'address', 'dept_id', 'designation'
        return rws

    def get_department_by_id(self, dept_id):
        logger.debug(f'{type(dept_id)}: {dept_id}')
        rws = self.cur.execute(GET_DEPT_DETAILS_BY_ID, (dept_id,)).fetchone()
        if rws is None:
            logger.info(INVALID_DEPT_ID)
            raise InvalidDepartmentIDException(THERE_WAS_SOME_PROBLEM)
        return rws

    def get_dept_name_id_mapping(self):
        rws = self.cur.execute(DEPT_TABLE_MAPPING_QUERY).fetchall()
        if rws.rowcount == 0:
            logger.info("Query for department details got 0 rows")
            raise NoDepartmentsException("There was some problem")
        mapping = {}
        for row in rws:
            mapping[row[1]] = row[0]
        return mapping


if __name__ == "__main__":
    conn = sqlite3.connect(r"C:\Users\mbhatnagar\PycharmProjects\CSM\csm.DBUtils")
    em = EmployeeDAO(conn)
    em.cur.execute("INSERT INTO dept_details VALUES('1','IT')")
    em.cur.execute("INSERT INTO dept_details VALUES('2','Sales')")
    em.cur.execute("INSERT INTO dept_details VALUES('3', 'QA')")
    e_id = shortuuid.ShortUUID().random(length=5)
    em.cur.execute("INSERT INTO emp_auth VALUES(?,'micheal_scott@gmail.com','MichealScott@1')", (e_id,))
    em.cur.execute("INSERT INTO emp_details VALUES(?,'MichealScott','6464646475', '1', 'Scranton,PA', 'Manager')", (e_id,))
    conn.commit()
    conn.close()
