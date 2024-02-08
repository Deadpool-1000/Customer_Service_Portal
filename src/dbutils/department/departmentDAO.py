from flask import current_app

logger = current_app.logger


class DepartmentDAO:
    """Context manager for department related operation. On exit, it closes the cursor it uses."""
    def __init__(self, conn):
        self.cur = conn.cursor(dictionary=True)

    def get_department_by_id(self, dept_id):
        """Get department with id as dept_id"""
        self.cur.execute(current_app.config['GET_DEPARTMENT_FROM_DEPT_ID'], {
            'dept_id': dept_id
        })
        logger.debug(f"DepartmentDAO: department with {dept_id} fetched.")
        return self.cur.fetchone()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            return False
        self.cur.close()
