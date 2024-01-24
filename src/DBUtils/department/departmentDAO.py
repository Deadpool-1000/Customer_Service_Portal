from src.DBUtils.config.queries_config_loader import QueriesConfig


class DepartmentDAO:
    def __init__(self, conn):
        self.cur = conn.cursor(dictionary=True)

    def get_department_by_id(self, dept_id):
        self.cur.execute(QueriesConfig.GET_DEPARTMENT_FROM_DEPT_ID, {
            'dept_id': dept_id
        })
        return self.cur.fetchone()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            return False
        self.cur.close()
