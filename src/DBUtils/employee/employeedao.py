import logging

from src.DBUtils.config.queries_config_loader import QueriesConfig


logger = logging.getLogger('main.employee_dao')


class EmployeeDAO:
    singleton = 1

    def __init__(self, conn):
        self.cur = conn.cursor(dictionary=True)
        if self.singleton != 0:
            self.cur.execute(QueriesConfig.CREATE_TABLE_DEPT_DETAILS)
            self.cur.execute(QueriesConfig.CREATE_TABLE_EMP_DETAILS)
            self.singleton -= 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            return False
        self.cur.close()

    def get_employee_details_by_id(self, e_id):
        self.cur.execute(QueriesConfig.GET_EMPLOYEE_DETAILS_BY_ID, {
            'e_id': e_id
        })
        emp_data = self.cur.fetchone()
        # 'e_id', 'full_name', 'phn_num', 'address', 'dept_id', 'designation'
        return emp_data

    def get_department_by_employee_id(self, e_id):
        self.cur.execute(QueriesConfig.GET_DEPARTMENT_FROM_EMP_ID, {
            'e_id': e_id
        })
        return self.cur.fetchone()
