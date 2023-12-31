import logging

from src.DBUtils.config.db_config_loader import DBConfig
from src.DBUtils.config.queries_config_loader import QueriesConfig
from src.utils.exceptions.exceptions import NoDepartmentsException, InvalidEmployeeIDException, \
    InvalidDepartmentIDException

logger = logging.getLogger('main.employee_dao')


class EmployeeDAO:
    singleton = 1

    def __init__(self, conn):
        self.cur = conn.cursor()
        if self.singleton != 0:
            self.cur.execute(QueriesConfig.CREATE_TABLE_DEPT_DETAILS)
            self.cur.execute(QueriesConfig.CREATE_TABLE_EMP_DETAILS)
            conn.commit()
            self.singleton -= 1

    def get_employee_details_by_id(self, e_id):
        rws = self.cur.execute(QueriesConfig.GET_EMPLOYEE_DETAILS_BY_ID, (e_id,)).fetchone()
        if rws is None:
            logger.info(DBConfig.INVALID_EMP_ID)
            raise InvalidEmployeeIDException(DBConfig.THERE_WAS_SOME_PROBLEM)
        # 'c_id', 'full_name', 'phn_num', 'address', 'dept_id', 'designation'
        return rws

    def get_department_by_id(self, dept_id):
        rws = self.cur.execute(QueriesConfig.GET_DEPT_DETAILS_BY_ID, (dept_id,)).fetchone()
        if rws is None:
            logger.info(DBConfig.INVALID_DEPT_ID)
            raise InvalidDepartmentIDException(DBConfig.THERE_WAS_SOME_PROBLEM)
        return rws
