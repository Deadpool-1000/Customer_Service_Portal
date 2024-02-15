from flask import current_app

from src.dbutils.base_dao import BaseDAO

logger = current_app.logger


class DepartmentDAO(BaseDAO):
    """Context manager for department related operation. On exit, it closes the cursor it uses."""

    def get_department_by_id(self, dept_id):
        """Get department with id as dept_id"""
        self.cur.execute(current_app.config['GET_DEPARTMENT_FROM_DEPT_ID'], {
            'dept_id': dept_id
        })
        logger.debug(f"DepartmentDAO: department with {dept_id} fetched.")
        return self.cur.fetchone()
