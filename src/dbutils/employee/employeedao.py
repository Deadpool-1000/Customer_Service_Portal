from flask import current_app

logger = current_app.logger


class EmployeeDAO:
    """Context manager for performing operation on employee. On exit, it closes the cursor it uses."""
    singleton = 1

    def __init__(self, conn):
        self.cur = conn.cursor(dictionary=True)
        if self.singleton != 0:
            self.cur.execute(current_app.config['CREATE_TABLE_DEPT_DETAILS'])
            self.cur.execute(current_app.config['CREATE_TABLE_EMP_DETAILS'])
            logger.debug("EmployeeDAO: Employee details and department details table created.")
            self.singleton -= 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            return False
        self.cur.close()

    def get_employee_details_by_id(self, e_id):
        """Gets employee details for employee e_id"""
        self.cur.execute(current_app.config['GET_EMPLOYEE_DETAILS_BY_ID'], {
            'e_id': e_id
        })
        emp_data = self.cur.fetchone()
        logger.debug(f"EmployeeDAO: employee details for employee with emp id {e_id} fetched.")
        # 'e_id', 'full_name', 'phn_num', 'address', 'dept_id', 'designation'
        return emp_data

    def get_department_by_employee_id(self, e_id):
        """Gets department details for employee e_id"""
        self.cur.execute(current_app.config['GET_DEPARTMENT_FROM_EMP_ID'], {
            'e_id': e_id
        })
        logger.debug(f"Department details for employee {e_id} fetched.")
        return self.cur.fetchone()
