import logging
from utils.exceptions import NoDepartmentsException
from DBUtils.config.db_config_loader import DBConfig
from DBUtils.config.queries_config_loader import QueriesConfig
from utils.exceptions import InvalidEmployeeIDException, InvalidDepartmentIDException


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

    def get_dept_name_id_mapping(self):
        rws = self.cur.execute(QueriesConfig.DEPT_TABLE_MAPPING_QUERY).fetchall()
        if rws.rowcount == 0:
            logger.error(f'Department table failed to return any row')
            raise NoDepartmentsException(DBConfig.THERE_WAS_SOME_PROBLEM)
        mapping = {}
        for row in rws:
            mapping[row[1]] = row[0]
        return mapping

